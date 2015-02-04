import ast

def read_file_user(db, recordid, appfolder, os):
    item = db.userfiles(db.userfiles.id == recordid) or None
    txt = os.path.join(appfolder, "uploads", item.userfile)
    data = filter(None, open(txt, 'r').read().split("\n")[1:])
    results = {}
    for record in data:
        print "record::", record
        record = record.split(",")
        rec_year = {}
        if len(record) > 13:
            values = record[1:-13]
        else:
            values = record[1:]
        for i,item in enumerate(values):
            rec_year[i+1] = [ast.literal_eval(item),0]
        results[record[0]] = rec_year
    return results


def delUserCharts(os, appfolder, user):
    print "will delete...", user
    for root, dirs, files in os.walk(appfolder+'/static/usercharts'):
        for f in files:
            if f.endswith("_"+str(user)+".png"):
                os.unlink(os.path.join(root, f))
        return "success"