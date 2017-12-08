from controllers.constructor import Constructor

try:
    build = Constructor("Usuario")
    build.create_model(model_name = "users", data = [
        {
            "id": 1,
            "name": "Guilherme"
        }
    ])
    build.view_page(page_name = "index", style = "material", template = "basic")
    build.select_model(model_name = "users")
    build.run()
except:
    raise