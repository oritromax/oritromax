import urllib2
import os
from bottle import get, post, request, run, Bottle

application = app = Bottle()

def get_result(exam, year, board, roll):
  base_url = "http://www.educationboardresults.gov.bd/regular"

	index_response = urllib2.urlopen(base_url + "/index.php")
	session_var = index_response.info().headers[3].split()[1][0:36]
	post_data = "sr=3&et=0&exam=%s&year=%s&board=%s&roll=%s&button2=Submit" % (exam, year, board, roll)

	result_request = urllib2.Request(base_url + "/result.php", headers = {'Cookie': session_var})
	result_response = urllib2.urlopen(result_request, post_data)
	return result_response.read()

@app.route('/')
def index_page():
	return '''<html><head><meta property="og:image" content="http://icons.iconarchive.com/icons/gakuseisean/ivista-2/128/Network-Upload-icon.png"/><title>Board Result Fetcher</title><meta name="description" content="Get your board result before anyone else does! (Probably, even before they get published)"></head>
		<body style="padding: 2em; font-family: Ubuntu, 'Segoe UI', Arial, sans-serif;">
		<h2>Board Result Fetcher</h2>
		<form action="/check" method="post" >
		Exam: <select name="exam">
                            <option value="hsc">HSC/Alim/Equivalent</option>
                            <option value="jsc">JSC/JDC</option>
                            <option value="ssc">SSC/Dakhil</option>
							<option value="ssc_voc">SSC(Vocational)</option>
                            <option value="hsc">HSC/Alim</option>
							<option value="hsc_voc">HSC(Vocational)</option>
							<option value="hsc_hbm">HSC(BM)</option>
							<option value="hsc_dic">Diploma in Commerce</option>
							<option value="hsc_dibs">Diploma in Business Studies</option>
                          </select><br />
		Year: <select id="year" name="year">
                            <option selected="" value="2013">2013</option><option value="2012">2012</option><option value="2011">2011</option><option value="2010">2010</option><option value="2009">2009</option><option value="2008">2008</option><option value="2007">2007</option><option value="2006">2006</option><option value="2005">2005</option><option value="2004">2004</option><option value="2003">2003</option><option value="2002">2002</option><option value="2001">2001</option><option value="2000">2000</option><option value="1999">1999</option><option value="1998">1998</option><option value="1997">1997</option><option value="1996">1996</option>
                          </select><br />
		Roll: <input name="roll" type="text" maxlength="6"/><br />
		Board: <select id="board" name="board">
                          <option selected="" value="">Select One</option>
						  <option value="barisal">Barisal</option>
						  <option value="chittagong">Chittagong</option>
						  <option value="comilla">Comilla</option>
                          <option value="dhaka">Dhaka</option>
						  <option value="dinajpur">Dinajpur</option>
						  <option value="jessore">Jessore</option>
                          <option value="rajshahi">Rajshahi</option>
                          <option value="sylhet">Sylhet</option>
                          <option value="madrasah">Madrasah</option>
						  <option value="tec">Technical</option>
						  <option value="dibs">DIBS(Dhaka)</option>
                          </select><br /><br />
		<input value="Check result" type="submit" />
		</form></body></html>'''

@app.route('/check', method="POST")
def result():
	roll = request.forms.get("roll")
	board = request.forms.get("board")
	exam = request.forms.get("exam")
	year = request.forms.get("year")
	result = get_result(exam, year, board, roll)
	if result == "Error: QDTL65656565":
		return '''<div style="margin: 1em 4em; padding: 1em; border: 1px solid #dd4814;"><h2>Result Database Tables not found</h2><p>The board site is having issues with their database, probably they have not yet uploaded and propagated the database tables for this years examinees, please keep patience and try a few minutes later.</p></div>'''
	else: return result

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=80)
