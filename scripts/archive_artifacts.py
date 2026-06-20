import argparse
import os
import shutil
import time
import zipfile


def archive_timestamp():
	# ZIP timestamps have a two-second resolution, so use an even second for both
	# the archive itself and every entry stored in it.
	return int(time.time()) & ~1


def add_directory(archive, archive_path, timestamp):
	info = zipfile.ZipInfo(archive_path.rstrip("/") + "/", time.localtime(timestamp)[:6])
	info.external_attr = (0o40775 << 16) | 0x10
	archive.writestr(info, b"")


def add_file(archive, source_path, archive_path, timestamp):
	info = zipfile.ZipInfo.from_file(source_path, archive_path)
	info.date_time = time.localtime(timestamp)[:6]
	info.compress_type = zipfile.ZIP_DEFLATED
	with open(source_path, "rb") as source, archive.open(info, "w") as destination:
		shutil.copyfileobj(source, destination)


def make_archive(archive_path, entries, directories=()):
	timestamp = archive_timestamp()
	with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
		for directory in directories:
			add_directory(archive, directory, timestamp)
		for source_path, stored_path in entries:
			add_file(archive, source_path, stored_path, timestamp)
	os.utime(archive_path, (timestamp, timestamp))


def make_rel_archive(a_args):
	make_archive(
		"{}.zip".format(a_args.name),
		[(a_args.dll, "F4SE/Plugins/{}".format(os.path.basename(a_args.dll)))],
		directories=("F4SE", "F4SE/Plugins"),
	)

def make_dbg_archive(a_args):
	make_archive(
		"{}_pdb.zip".format(a_args.name),
		[
			(a_args.pdb, os.path.basename(a_args.pdb)),
			(a_args.dll, os.path.basename(a_args.dll)),
		],
	)

def parse_arguments():
	parser = argparse.ArgumentParser(description="archive build artifacts for distribution")
	parser.add_argument("--dll", type=str, help="the full dll path", required=True)
	parser.add_argument("--name", type=str, help="the project name", required=True)
	parser.add_argument("--pdb", type=str, help="the full pdb path", required=True)
	return parser.parse_args()

def main():
	out = "artifacts"
	try:
		os.mkdir(out)
	except FileExistsError:
		pass
	os.chdir(out)

	args = parse_arguments()
	make_rel_archive(args)
	make_dbg_archive(args)

if __name__ == "__main__":
	main()
