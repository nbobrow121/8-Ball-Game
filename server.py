import sys
import os
import cgi
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl, parse_qs
import Physics

current_player = random.randint(1, 2)

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse(self.path)
        
		if parsed.path in ['/mainpage.html', '/script.js', '/style.css']:
			filename = '.' + parsed.path
            
			if os.path.exists(filename):
                
				with open(filename, 'r') as file:
					content = file.read()
                
				content_type = "text/html" if parsed.path.endswith('.html') else \
                               "application/javascript" if parsed.path.endswith('.js') else \
                               "text/css"
                
				self.send_response(200)
				self.send_header("Content-type", content_type)
				self.send_header("Content-length", len(content))
				self.end_headers()
				self.wfile.write(bytes(content, "utf-8"))
            
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))
        
		elif parsed.path.startswith('/animation'):
			query_params = dict(parse_qsl(parsed.query))
			time = float(query_params.get('time', 0.0))
			db = Physics.Database()
			cur = db.conn.cursor()
            
			cur.execute("SELECT TABLEID FROM TTable WHERE TIME = ?", (time,))
			result = cur.fetchone()
			table = db.readTable(result[0] - 1)
            
			cur.close()
			db.conn.commit()
			db.conn.close()
            
			svg_string = table.svg()
			self.send_response(200)
			self.send_header('Content-type', 'image/svg+xml')
			self.end_headers()
            
			self.wfile.write(svg_string.encode('utf-8'))
        
		elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
			filename = parsed.path[1:]
			filepath = os.path.join('.', filename)
            
			if os.path.exists(filepath):
                
				with open(filepath, 'rb') as file:
					content = file.read()
                
				self.send_response(200)
				self.send_header('Content-type', 'image/svg+xml')
				self.end_headers()
                
				self.wfile.write(content)
            
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))
		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

	def do_POST(self):
		parsed = urlparse(self.path)
        
		if parsed.path == '/display.html':
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']})
			p1name = form.getvalue('p1name', 'Player 1')
			p2name = form.getvalue('p2name', 'Player 2')
            
			game = Physics.Game(gameName="Game 01", player1Name=p1name, player2Name=p2name)
			new_table = Physics.setupTable()
			db = Physics.Database()
			table_id = db.writeTable(new_table)
            
			cur = db.conn.cursor()
            
			cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES( ?,  ?);", (table_id + 1, 0))
            
			cur.close()
			db.conn.commit()
            
			html_string = f'''<html><head><title>8-Ball Game!</title>
                            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                            <link rel="stylesheet" href="styles.css"></head>
                            <body style="text-align: center;"> <h1>Pool Table</h1>
                            <body style="text-align: center;"> <h2>Player 1:</h2>
                            <div class="container"><div class="player" id="player1"><h2>{p1name}</h2></div>
                            '''
			table_svg = new_table.svg().replace('width="700"', 'width="350"').replace('height="1375"', 'height="687.5"')
			table_svg = table_svg.replace('</svg>', '<line id="line" x1="0" y1="0" x2="0" y2="0"/></svg>')
			html_string += f'<object id="svg-object"> {table_svg}</object>'
			html_string += '''<button class="exit"><a href="/mainpage.html">Exit Game</a></button>
                            <body style="text-align: center;"> <h2>Player 2:</h2>
                            <div class="player" id="player2"><h2>{}</h2></div></div>
                            <script src="script.js"></script></body></html>'''.format(p2name)
            
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes(html_string, 'utf-8'))
        
		elif parsed.path == '/game.html':
			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length).decode('utf-8')
			post_params = parse_qs(post_data)
            
			x = float(post_params.get('x', [''])[0])
			y = float(post_params.get('y', [''])[0])
            
			for filename in os.listdir('.'):
                
				if filename.startswith('table-') and filename.endswith('.svg'):
					os.remove(filename)
            
			game = Physics.Game(gameID=0)
			db = Physics.Database()
			cur = db.conn.cursor()
            
			cur.execute("SELECT TABLEID FROM TTable;")
            
			table_ids = cur.fetchall()
			original_ids = len(table_ids) - 1
			cur_table = db.readTable(original_ids)
            
			cur.close()
			db.conn.commit()
            
			print("Player1: ", game.player1Name, " Player2:", game.player2Name," Game name: ", game.gameName, " Table ID count: ", len(table_ids))
			print("x is ", x, "and y is ", y)

			game.shoot(game.gameName, game.player1Name, table=cur_table, xvel=x, yvel=y)
            
			cur = db.conn.cursor()
			cur.execute("SELECT TABLEID FROM TableShot;")
            
			table_ids = cur.fetchall()

			print("table id: ", len(table_ids))
            
			svg_string = ""
            
			for i in range(original_ids, len(table_ids)):
				table = db.readTable(i)
				start_index = table.svg().find('<rect')
				end_index = table.svg().find('WHITE" />') + len('WHITE" />')
				table_svg = table.svg()[start_index:end_index]
				table_svg += '<line id="line" x1="0" y1="0" x2="0" y2="0" stroke="red" stroke-width="5"/>'
				svg_string += table_svg + ","
            
			if game.isGameOver(table):
				return None
            
			else:
				svg_string = svg_string[:-1]
            
			cur.close()
			db.conn.commit()
			db.conn.close()
            
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(svg_string.encode('utf-8'))
        
		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python server.py <port>")
		sys.exit(1)
	port = int(sys.argv[1])
	httpd = HTTPServer(('localhost', port), MyHandler)
	print("Server listening on port:", port)
	httpd.serve_forever()