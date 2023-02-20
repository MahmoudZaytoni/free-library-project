from website import create_app
from flask import render_template

app = create_app()

# Create Custom Error Pages

# - Invalid Url 
@app.errorhandler(404)
def page_not_found(e):
  type_error = "404 Error"
  message = "Page Not Found"
  return render_template("base-error.html", type_error=type_error, message=message), 404

# - Internal Server Error
@app.errorhandler(500)
def server_error(e):
  type_error = "505 Internal Server Error"
  message = "Try Again.."
  return render_template("500.html"), 500

if __name__ == "__main__":
  app.run()
