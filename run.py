from app import app,r

if __name__ == '__main__':
    # r.set("PV", 0)
    # r.set("ALL", 1)
    # r.set("SUCCESS", 0)
    app.run(debug=True)

application = app