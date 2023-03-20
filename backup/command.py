import os
from basescript import BaseScript
from backup.upload.upload import Upload


class Backup(BaseScript):
    DESC = "Backup command-line tool"

    def upload(self):
        u = Upload(self.args, self.log)
        u.run()

    def define_subcommands(self, subcommands):
        super(Backup, self).define_subcommands(subcommands)

        upload = subcommands.add_parser("upload", help="upload files")
        upload.set_defaults(func=self.upload)
        upload.add_argument("--input-dir", default=".", help="Media location to upload")

def main():
    Backup().start()

if __name__ == "__main__":
    main()
