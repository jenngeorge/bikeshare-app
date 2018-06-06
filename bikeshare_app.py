from flask import Flask, Response
# from consumer import station_consumer

#Continuously listen to the connection and print messages as recieved
app = Flask(__name__)

@app.route('/')


# def index():
#     return Response(kafkastream(),
#                     mimetype='text')
# def kafkastream():
#     for msg in station_consumer:
#         yield msg.value

def index():
    return "hello!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
