
import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QMessageBox
)

from src.caller import initialize_application, ask_question


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"


class DesktopApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.vector_store = None
        self.llm = None

        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

        self.setWindowTitle("Assistente Inteligente de Documentos")
        self.setMinimumSize(850, 600)

        self.setup_ui()
        self.load_existing_documents()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)

        # Título
        title = QLabel("Assistente de Documentos")
        title.setObjectName("title")

        subtitle = QLabel(
            "Consulte informações presentes nos seus documentos."
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Upload de documentos
        upload_layout = QHBoxLayout()

        self.upload_button = QPushButton("Adicionar documentos PDF")
        self.upload_button.clicked.connect(self.add_documents)

        self.status_label = QLabel("Nenhum documento processado.")
        self.status_label.setObjectName("status")

        upload_layout.addWidget(self.upload_button)
        upload_layout.addWidget(self.status_label)

        layout.addLayout(upload_layout)

        # Campo de pergunta
        question_label = QLabel("Faça sua pergunta")

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Digite sua pergunta sobre os documentos..."
        )

        self.ask_button = QPushButton("Enviar pergunta")
        self.ask_button.clicked.connect(self.ask_question)

        layout.addWidget(question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(self.ask_button)

        # Área de resposta
        answer_label = QLabel("Resposta")

        self.answer_area = QTextEdit()
        self.answer_area.setReadOnly(True)
        self.answer_area.setPlaceholderText(
            "As respostas aparecerão aqui..."
        )

        layout.addWidget(answer_label)
        layout.addWidget(self.answer_area)

        # Estilização
        self.setStyleSheet("""
            QMainWindow {
                background-color: #171c1a;
            }

            QLabel {
                color: #e5e7eb;
                font-size: 14px;
            }

            QLabel#title {
                color: #ffffff;
                font-size: 27px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #9ca3af;
                font-size: 13px;
            }

            QLabel#status {
                color: #9ca3af;
                font-size: 12px;
            }

            QLineEdit, QTextEdit {
                background-color: #252d29;
                color: #f3f4f6;
                border: 1px solid #37443d;
                border-radius: 7px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 11px 16px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #157347;
            }

            QPushButton:disabled {
                background-color: #46534b;
                color: #a7b0aa;
            }
        """)

    def load_existing_documents(self):

        pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

        if not pdf_files:
            self.status_label.setText("Nenhum documento encontrado.")
            return

        self.status_label.setText("Carregando documentos...")

        self.upload_button.setEnabled(False)
        self.ask_button.setEnabled(False)

        try:

            self.vector_store, self.llm, errors = initialize_application()

            self.status_label.setText(
                f"{len(pdf_files)} documento(s) carregado(s)."
            )

            if errors:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    "\n".join(errors)
                )

        except Exception as error:

            self.status_label.setText("Erro ao carregar documentos.")

            QMessageBox.critical(
                self,
                "Erro",
                str(error)
            )

        finally:
            self.upload_button.setEnabled(True)
            self.ask_button.setEnabled(True)

    def add_documents(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar documentos PDF",
            str(DOCUMENTS_DIR),
            "Arquivos PDF (*.pdf)"
        )

        if not files:
            return

        added = []
        duplicates = []

        existing_names = {
            file.name.casefold()
            for file in DOCUMENTS_DIR.glob("*.pdf")
        }

        for file in files:

            source = Path(file)
            filename = source.name

            # Verifica se já existe um documento com o mesmo nome
            if filename.casefold() in existing_names:
                duplicates.append(filename)
                continue

            try:

                destination = DOCUMENTS_DIR / filename

                shutil.copy2(source, destination)

                existing_names.add(filename.casefold())
                added.append(filename)

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Erro ao copiar documento",
                    f"{filename}: {error}"
                )

        if not added:

            QMessageBox.information(
                self,
                "Documentos",
                "Nenhum documento novo foi adicionado."
            )

            return

        self.status_label.setText("Processando documentos...")

        self.upload_button.setEnabled(False)
        self.ask_button.setEnabled(False)

        try:

            # Atualiza a base de conhecimento
            self.vector_store, self.llm, errors = initialize_application()

            total_documents = len(list(DOCUMENTS_DIR.glob("*.pdf")))

            self.status_label.setText(
                f"Base atualizada. {total_documents} PDF(s)."
            )

            message = f"Documentos adicionados: {len(added)}"

            if duplicates:
                message += (
                    "\n\nDocumentos ignorados por duplicidade:\n"
                    + "\n".join(duplicates)
                )

            if errors:
                message += (
                    "\n\nProblemas encontrados:\n"
                    + "\n".join(errors)
                )

            QMessageBox.information(
                self,
                "Processamento concluído",
                message
            )

        except Exception as error:

            self.status_label.setText("Erro no processamento.")

            QMessageBox.critical(
                self,
                "Erro",
                str(error)
            )

        finally:
            self.upload_button.setEnabled(True)
            self.ask_button.setEnabled(True)

    def ask_question(self):

        question = self.question_input.text().strip()

        if not question:
            QMessageBox.warning(
                self,
                "Pergunta vazia",
                "Digite uma pergunta."
            )
            return

        if self.vector_store is None or self.llm is None:

            QMessageBox.warning(
                self,
                "Base indisponível",
                "Adicione documentos antes de fazer perguntas."
            )
            return

        self.ask_button.setEnabled(False)
        self.upload_button.setEnabled(False)

        self.answer_area.setPlainText("Analisando documentos...")

        try:

            answer, sources = ask_question(
                self.vector_store,
                self.llm,
                question
            )

            result = answer

            result += "\n\n------------------------------"
            result += "\nFONTES UTILIZADAS:\n"

            result += "\n".join(
                f"- {source}"
                for source in sources
            )

            self.answer_area.setPlainText(result)

        except Exception as error:

            self.answer_area.setPlainText(
                "Não foi possível responder à pergunta."
            )

            QMessageBox.critical(
                self,
                "Erro na consulta",
                str(error)
            )

        finally:
            self.ask_button.setEnabled(True)
            self.upload_button.setEnabled(True)


def start_desktop_app():

    app = QApplication([])

    window = DesktopApp()
    window.show()

    app.exec()
