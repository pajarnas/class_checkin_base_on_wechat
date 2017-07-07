def sum_format(sum_records,seq_id=0):
    keys = sum_records[0].keys()
    keys.remove('StuID')
    if seq_id == 0:
        for i in range(1,len(keys)):
            print '================================='
            print '%s\t\t\t%s\t' % ('StuID','checkin'+str(i))
            for j in sum_records:
                print '%s\t%s\t' % (j['StuID'],j['checkin'+str(i)])
            else:
                print '================================='
    else:
        print '================================='
        print '%s\t\t\t%s\t' % ('StuID', 'checkin' + str(seq_id))
        for j in sum_records:
            print '%s\t%s\t' % (j['StuID'], j['checkin' + str(seq_id)])
        else:
            print '================================='

def detail_format(detail_records):
    keys = detail_records[0].keys()
    keys.remove('StuID')
    print '=================================================================================='
    print '%s\t\t%s\t\t%s\t%s\t%s\t%s\t' % ('StuID', 'checkinTime','ProofPath','IsSuc','Type' ,'Result')
    for i in detail_records:
        print '%s\t%s\t%s\t\t%s\t%s\t%s\t' % (i['StuID'], i['checkinTime'],i['ProofPath'],i['IsSuc'],i['checkinType'] ,i['checkinResult'])
    else:
        print '=================================================================================='

