from flask import Flask
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
from flask import redirect
from app.module import dbModule

main = Blueprint('main', __name__, url_prefix='/main')
app = Flask(__name__)
app.secret_key = 'some_secret'


@main.route('/', methods=['GET'])
def index():
    testData = 'testData array'

    return render_template('/main/index.html')

#base62 algorithm
def make_shorten(v):
    CODEC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ret = []
    while v > 0:
        v, idx = divmod(v, 62)
        ret.insert(0, CODEC[idx])

    return ''.join(ret)

#url 라빈카프
def string_to_myNum(myStr):
    ascii_list = [ord(ch) for ch in myStr]
    mul = 1
    myNum = 1
    # print(ascii_list)
    for c in ascii_list:
        myNum += mul * int(c)
        mul = mul * 2
    return myNum


def check_intro(init_url):
    if init_url[:8] == 'https://':
        return init_url[8:]
    elif init_url[:7] == 'http://':
        return init_url[7:]
    return init_url


@main.route('/send', methods=['POST'])
def send():
    input_url = check_intro(request.form['input_u'])
    if (input_url == ''):
        return render_template('/main/index.html',
                               result='please input URL!')
    ascii_url = string_to_myNum(input_url)
    shorten = make_shorten(ascii_url)

    db_class = dbModule.Database()
    sql1 = "SELECT shorten FROM shortenDB.shortenTable WHERE origin_url = '%s'" % input_url;
    check = db_class.executeAll(sql1)
    result_msg = ''
    if check:  # 이미 존재하는 url
        result_msg = 'already done!'
    else:  # 존재하지 않는 url인 경우 새로 추가
        print('check 0')
        check_already = "SELECT count(*) FROM shortenDB.shortenTable WHERE shorten = '%s'" % shorten;
        sameShortenCnt = db_class.executeAll(check_already)

        sql = "INSERT INTO shortenDB.shortenTable VALUES('%s','%s',%d)" % (
        input_url, shorten, sameShortenCnt[0]['count(*)'])
        db_class.execute(sql)
        db_class.commit()
        result_msg = 'insert is done!'
        db_class.commit()
    return render_template('/main/index.html',
                           searchURL='http://' + input_url,
                           result=result_msg,
                           shorten_url='http://127.0.0.1:5000/main/' + shorten)

#shorten URL 입력
@main.route('/<name>', methods=['GET','POST'])
def handle_shorten(name):
    db_class = dbModule.Database()
    sql1 = "SELECT origin_url FROM shortenDB.shortenTable WHERE shorten = '%s'" % name;
    check = db_class.executeAll(sql1)
    if(check):
        print('http://'+check[0]['origin_url'])
        return redirect('http://'+check[0]['origin_url'])
    else:
         return render_template('/main/index.html')
#
if __name__ == "__main__":
    app.run(debug=True)
