def check_files():
    # demo.func1()
    if request.method == 'POST':
        try:
            file1 = request.files['file1']
            file2 = request.files['file2']
            global filename
            filename = secure_filename(file2.filename)
            path = os.path.abspath(filename)
            open('code/file.txt', 'w').write(filename)
            # print(filename)
            # print(path)

            msg1 = ''
            msg2 = ''
            sm = ""
            if file1:
                msg1 = 'file 1 recieved'
            else:
                msg1 = 'file 1 not recieved'
            if file2:
                msg2 = 'file 2 recieved'
            else:
                msg2 = 'file 2 not recieved'

            h1 = hashlib.sha1()
            h2 = hashlib.sha1()
            chunk = 0
            while chunk != b'':
                chunk = file1.read(1024)
                h1.update(chunk)
            chunk = 0
            while chunk != b'':
                chunk = file2.read(1024)
                h2.update(chunk)
            shamsg1 = h1.hexdigest()
            shamsg2 = h2.hexdigest()
            # print(msg1 + "\n" + msg2)
            sm = (SequenceMatcher(None, shamsg1, shamsg2).ratio()*100)

            # print(sm)

            # return jsonify (
            #     {
            # 'status': True,
            # 'message1': msg1,
            # 'message2': msg2,
            # 'sm':sm

            #     },
            # )
            if sm < 100:
                # Repair the file
                subprocess.run(["ffmpeg", "-i", file1.filename,
                               "-c", "copy", "repaired_" + file1.filename])
                subprocess.run(["ffmpeg", "-i", file2.filename,
                               "-c", "copy", "repaired_" + file2.filename])
                return "Files corrupted. Repaired files are saved as repaired_file1.filename and repaired_file2.filename."
