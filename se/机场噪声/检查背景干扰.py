import xlwings,os
app=xlwings.App(visible=True,add_book=False)

for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\待计算'):
    for filexlsx in files:
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            file24=app.books.open(os.path.join(root,filexlsx))
            sht0=file24.sheets[0]
            for i in range(1,1824):
                eval=sht0.range('e{}'.format(i)).value
                fval=sht0.range('f{}'.format(i)).value
                kval = sht0.range('k{}'.format(i)).value
                # print(eval,fval,kval)
                if eval==None and (fval not in [None,'航班信息']):
                    if kval==None:
                        print(filexlsx,'['+str(i)+']','缺')
                    elif kval=='航班重合':
                        print(filexlsx,'['+str(i)+']','航班重合')
                if eval!=None and fval!=None:
                    if kval not in[None,'备注']:
                        print(filexlsx,'['+str(i)+']','多')
            file24.close()
            try:
                os.remove(os.path.join(root, filexlsx))
            except:pass
app.quit()