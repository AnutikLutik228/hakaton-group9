class EmailMover:
    def move(self, src_path, category):
        if category is None:
            dest_dir = "broken"
        else:
            dest_dir = category
        os.makedirs(dest_dir, exist_ok=True)
