class MessageHandlerFile:
    def create_file(self, filename: str):
        try:
            with open('docs/readme.txt', 'w') as f:
                f.write('Create a new text file!')
        except FileNotFoundError:
            print("The 'docs' directory does not exist")

    def read_file(self, filename):
        try:
            with open(filename, 'r') as f:
                contents = f.read()
                print(contents)
        except IOError:
            print("Error: could not read file " + filename)

    def append_file(self, filename, text):
        try:
            with open(filename, 'a') as f:
                f.write(text)
            print("Text appended to file " + filename + " successfully.")
        except IOError:
            print("Error: could not append to file " + filename)

    def rename_file(filename, new_filename):
        try:
            os.rename(filename, new_filename)
            print("File " + filename + " renamed to " + new_filename + " successfully.")
        except IOError:
            print("Error: could not rename file " + filename)

    def delete_file(filename):
        try:
            os.remove(filename)
            print("File " + filename + " deleted successfully.")
        except IOError:
            print("Error: could not delete file " + filename)