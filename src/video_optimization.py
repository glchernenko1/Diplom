import io
import struct
import collections

CHUNK_SIZE = 8192

Atom = collections.namedtuple('Atom', ['name', 'position', 'size'])


def read_atom(datastream):
    size, type = struct.unpack(">L4s", datastream.read(8))
    type = type.decode('ascii')
    return size, type


def _read_atom_ex(datastream):
    pos = datastream.tell()
    atom_size, atom_type = read_atom(datastream)
    if atom_size == 1:
        atom_size, = struct.unpack(">Q", datastream.read(8))
    return Atom(atom_type, pos, atom_size)


def get_index(datastream):
    index = list(_read_atoms(datastream))
    _ensure_valid_index(index)
    return index


def _read_atoms(datastream):
    datastream.seek(0)
    while datastream:
        try:
            atom = _read_atom_ex(datastream)
        except:
            break
        yield atom

        if atom.size == 0:
            if atom.name == "mdat":
                break
            else:
                continue
        datastream.seek(atom.position + atom.size)


def _ensure_valid_index(index):
    top_level_atoms = set(item.name for item in index)
    for key in ["moov", "mdat"]:
        if key not in top_level_atoms:
            msg = "%s atom not found, is this a valid MOV/MP4 file?" % key
            raise ValueError(msg)


def find_atoms(size, datastream):
    fake_parent = Atom('fake', datastream.tell() - 8, size + 8)
    for atom in _find_atoms_ex(fake_parent, datastream):
        yield atom.name


def _find_atoms_ex(parent_atom, datastream):
    stop = parent_atom.position + parent_atom.size

    while datastream.tell() < stop:
        try:
            atom = _read_atom_ex(datastream)
        except:
            msg = "Error reading next atom!"
            raise ValueError(msg)

        if atom.name in ["trak", "mdia", "minf", "stbl"]:
            for res in _find_atoms_ex(atom, datastream):
                yield res
        elif atom.name in ["stco", "co64"]:
            yield atom
        else:
            datastream.seek(atom.position + atom.size)


def _moov_is_compressed(datastream, moov_atom):
    datastream.seek(moov_atom.position + 8)
    stop = moov_atom.position + moov_atom.size
    while datastream.tell() < stop:
        child_atom = _read_atom_ex(datastream)
        datastream.seek(datastream.tell() + child_atom.size - 8)
        if child_atom.name == 'cmov':
            return True
    return False


def processing(datastream, limit=float('inf'), cleanup=True):
    outfile = io.BytesIO()
    index = get_index(datastream)

    mdat_pos = 999999
    free_size = 0

    for atom in index:
        if atom.name == "moov":
            moov_atom = atom
            moov_pos = atom.position
        elif atom.name == "mdat":
            mdat_pos = atom.position
        elif atom.name == "free" and atom.position < mdat_pos and cleanup:
            free_size += atom.size
        elif atom.name == "\x00\x00\x00\x00" and atom.position < mdat_pos:
            free_size += 8

    offset = - free_size
    if moov_pos < mdat_pos:
        return datastream
    else:
        offset += moov_atom.size

    is_compressed = _moov_is_compressed(datastream, moov_atom)
    if is_compressed:
        msg = "Movies with compressed headers are not supported"
        raise ValueError(msg)

    moov = _patch_moov(datastream, moov_atom, offset)

    for atom in index:
        if atom.name == "ftyp":
            datastream.seek(atom.position)
            outfile.write(datastream.read(atom.size))

    _write_moov(moov, outfile)

    skip_atom_types = ["ftyp", "moov"]
    if cleanup:
        skip_atom_types += ["free"]

    atoms = [item for item in index if item.name not in skip_atom_types]
    for atom in atoms:
        datastream.seek(atom.position)

        cur_limit = limit or float('inf')
        cur_limit = min(cur_limit, atom.size)

        for chunk in get_chunks(datastream, CHUNK_SIZE, cur_limit):
            outfile.write(chunk)
    datastream.close()
    return outfile


def _write_moov(moov, outfile):
    bytes = moov.getvalue()
    outfile.write(bytes)


def _patch_moov(datastream, atom, offset):
    datastream.seek(atom.position)
    moov = io.BytesIO(datastream.read(atom.size))

    atom = _read_atom_ex(moov)

    for atom in _find_atoms_ex(atom, moov):
        ctype, csize = dict(
            stco=('L', 4),
            co64=('Q', 8),
        )[atom.name]

        version, entry_count = struct.unpack(">2L", moov.read(8))

        entries_pos = moov.tell()

        struct_fmt = ">%(entry_count)s%(ctype)s" % vars()

        entries = struct.unpack(struct_fmt, moov.read(csize * entry_count))

        offset_entries = [entry + offset for entry in entries]
        moov.seek(entries_pos)
        moov.write(struct.pack(struct_fmt, *offset_entries))
    return moov


def get_chunks(stream, chunk_size, limit):
    remaining = limit
    while remaining:
        chunk = stream.read(min(remaining, chunk_size))
        if not chunk:
            return
        remaining -= len(chunk)
        yield chunk
