import os
import shutil
class EmailMover:
    def move(self, src_path, category):
        if category is None:
            dest_dir = "broken"
        else:
            dest_dir = category

        os.makedirs(dest_dir, exist_ok=True)

        file_name = os.path.basename(src_path)
        dst_path = os.path.join(dest_dir, file_name)

        if os.path.exists(dst_path):
            name, ext = os.path.splitext(file_name)
            number = 1

            while os.path.exists(dst_path):
                new_file_name = name + "_" + str(number) + ext
                dst_path = os.path.join(dest_dir, new_file_name)
                number += 1

        shutil.move(src_path, dst_path)

        if category is None:
            with open("run.log", "a", encoding="utf-8") as log:
                log.write("Broken file moved: " + src_path + "\n")

        return dst_path
