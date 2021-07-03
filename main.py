from src import cipher

from flask import Flask, render_template, request, redirect


app = Flask(__name__)




@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        result = cipher.apply_cypher(
            input_type = request.form.get("tipoEntrada"),
            algorithm = request.form.get("criptografiaSelecionada"),
            operation = request.form.get("operacaoSelecionada"),
            keywords = request.form.get("chave"),
            message = request.form.get("nome"),
            filename = request.form.get("caminhoArquivo"))

        print(result)   #TODO: save file here
        with open("output/cifrado.txt", "w") as file:
            file.write(result)

        return redirect("/")



if __name__ == "__main__":
    app.run(debug = True)