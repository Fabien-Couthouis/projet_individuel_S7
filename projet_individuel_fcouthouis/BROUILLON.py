if "author" in "I am the author":
    print("1 ok")

if "author" in "I am theauthor":
    print("2 ok")

if "author" in "I am the:author":
    print("3 ok")

if ("author" or "by") in "og:article:author":
    print("4 ok")
