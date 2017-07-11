def sum_format(sum_records,seq_id=0):
    if sum_records == []:
        return
    keys = sum_records[0].keys()
    if seq_id == 0:
        for i in range(1,len(keys)):
            print '================================='
            print '%s\t\t%s\t' % ('StuID','checkin'+str(i))
            for j in sum_records:
                print '%s\t%s\t' % (j['StuID'],j['checkin'+str(i)])
            else:
                print '================================='
    else:
        print '================================='
        print '%s\t\t%s\t' % ('StuID', 'checkin' + str(seq_id))
        for j in sum_records:
            print '%s\t%s\t' % (j['StuID'], j['checkin' + str(seq_id)])
        else:
            print '================================='


def detail_format(detail_records):

    if detail_records == []:
        return
    print '=================================================================================='
    print '%s\t\t%s\t\t%s\t\t%s\t%s\t%s\t' % ('StuID', 'checkinTime','ProofPath','IsSuc','Type' ,'Result')
    for i in detail_records:
        print '%s\t%s\t%s\t\t\t%s\t%s\t%s\t' % (str(i['StuID']), i['checkinTime'],i['ProofPath'],i['IsSuc'],i['checkinType'] ,i['checkinResult'])
    else:
        print '=================================================================================='


