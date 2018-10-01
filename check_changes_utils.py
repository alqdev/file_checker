# -*- coding: utf-8 -*-


def check_changes(feed_data, new_data):
        added_files = []
        changed_files = []
        deleted_files = []

        feed_files = feed_data.get('files', None)
        feed_subfolders = feed_data.get('subfolders', None)

        feed_files_names = [f_name.get('file_name') for f_name in feed_files]
        feed_subfolders_names = [f_name.get('folder_name') for f_name in feed_subfolders]
        total_feed = feed_files_names + feed_subfolders_names

        new_files = new_data.get('files', None)
        new_subfolders = new_data.get('subfolders', None)

        new_files_names = [f_name.get('file_name') for f_name in new_files]
        new_subfolders_names = [f_name.get('folder_name') for f_name in new_subfolders]
        total_new = new_files_names + new_subfolders_names

        if sorted(total_feed) == sorted(total_new):
            return None
        else:
            if new_files:
                for new_file in new_files:
                    file_name = new_file.get('file_name')
                    if file_name not in feed_files_names:
                        added_files.append(
                            {'file_name': file_name},
                        )

            if feed_files:
                for feed_file in feed_files:
                    file_name = feed_file.get('file_name')
                    if file_name not in new_files_names:
                        deleted_files.append(
                            {'file_name': file_name},
                        )

            if new_subfolders:
                for new_folder in new_subfolders:
                    folder_name = new_folder.get('folder_name')
                    if folder_name not in feed_subfolders_names:
                        added_files.append(
                            {'folder_name': folder_name}
                        )

            if feed_subfolders:
                for feed_folder in feed_subfolders:
                    folder_name = feed_folder.get('folder_name')
                    if folder_name not in new_subfolders_names:
                        deleted_files.append(
                            {'folder_name': folder_name}
                        )

            return {
                'files': new_files,
                'subfolders': new_subfolders,
                'added': added_files,
                'deleted': deleted_files,
            }


