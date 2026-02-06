from app import create_app

app = create_app()

@app.route('/', methods=['GET'])
def greetings():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
