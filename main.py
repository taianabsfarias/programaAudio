


import sys
import os
import csv

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSvgWidgets import *
from catalogar_audio import catalogar_audio


EXTENSOES_AUDIO = ['.wav', '.mp3', '.flac', '.ogg', '.aac']\

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa Som")
        self.resize(720, 600)
        self.lista_audios = []
        self.setup_ui()

    def setup_ui(self):
        widget_central = QWidget()
        layout_vertical = QVBoxLayout()
        layout_horizontal = QHBoxLayout()

        self.botao_arquivos = QPushButton("Selecionar arquivos de áudios")
        self.botao_arquivos.clicked.connect(self.selecionar_arquivos)

        self.botao_pasta = QPushButton("Selecionar pasta de áudios")
        self.botao_pasta.clicked.connect(self.selecionar_pasta)

        self.botao_csv = QPushButton("Exportar CSV")
        self.botao_csv.setEnabled(False)
        self.botao_csv.clicked.connect(self.exportar_csv)

        self.tabela_audios = QTableWidget()
        self.tabela_audios.setColumnCount(6)
        self.tabela_audios.setHorizontalHeaderLabels([
            "Arquivo", "Loudness", "Sharpness", "Strength",
            "Roughness", "Tonality"
        ])
        self.tabela_audios.setColumnWidth(3, 150) 
        self.tabela_audios.setColumnWidth(5, 150) 
        layout_horizontal.addWidget(self.botao_arquivos)
        layout_horizontal.addWidget(self.botao_pasta)

        layout_vertical.addLayout(layout_horizontal)
        layout_vertical.addWidget(self.tabela_audios)
        layout_vertical.addWidget(self.botao_csv)

        widget_central.setLayout(layout_vertical)
        self.setCentralWidget(widget_central)

    def selecionar_arquivos(self):
        arquivos,_ = QFileDialog.getOpenFileNames(
            self, "Selecionar arquivos de áudio", "",
            "Áudios (*.wav *.mp3 *.flac *.ogg *.aac)"
        )
        if arquivos:
            self.catalogar_audios(arquivos)

    def selecionar_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if pasta_selecionada:
            arquivos = [
                os.path.join(pasta_selecionada, arquivo)
                for arquivo in os.listdir(pasta_selecionada)
                if os.path.splitext(arquivo)[1].lower() in EXTENSOES_AUDIO
            ]
            self.catalogar_audios(arquivos)

    def catalogar_audios(self, arquivos):
        self.lista_audios = []
        self.tabela_audios.setRowCount(0)

        for caminho in arquivos:
            try:
                dados = catalogar_audio(caminho)
                nome = os.path.basename(caminho)

                self.lista_audios.append((nome, dados))

                linha = self.tabela_audios.rowCount()
                self.tabela_audios.insertRow(linha)
                self.tabela_audios.setItem(linha, 0, QTableWidgetItem(nome))

                for i, chave in enumerate(["loudness", "sharpness", "strength", "roughness", "tonality"]):
                    valor = str(dados.get(chave, "-"))
                    self.tabela_audios.setItem(linha, i + 1, QTableWidgetItem(valor))

            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao analisar:\n{caminho}\n\n{str(e)}")

        self.botao_csv.setEnabled(bool(self.lista_audios))

    def exportar_csv(self):
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar como", "", "CSV Files (*.csv)")
        if not caminho:
            return

        try:
            with open(caminho, "w", newline='', encoding="utf-8") as arquivo_csv:
                gerenciador_csv = csv.writer(arquivo_csv)
                gerenciador_csv.writerow(["Arquivo", "Loudness", "Sharpness", "Strength", "Roughness", "Tonality"])
                for nome, dados in self.lista_audios:
                    gerenciador_csv.writerow([
                        nome,
                        dados.get("loudness", ""),
                        dados.get("sharpness", ""),
                        dados.get("strength", ""),
                        dados.get("roughness", ""),
                        dados.get("tonality", ""),
                        dados.get("pitch", "")
                    ])
            QMessageBox.information(self, "Sucesso", "CSV exportado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao exportar CSV:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()  
    sys.exit(app.exec()) 

