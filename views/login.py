from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from database.database import database_manager
from styles.theme import PALETTE, SPACING, Typography


class LoginDialog(QDialog):
    """
    Login and registration window for PulseMind.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.user = None

        # ---------------------------------------------------------
        # Window setup
        # ---------------------------------------------------------

        self.setWindowTitle("PulseMind Login")

        self.setMinimumSize(
            520,
            620,
        )

        self.resize(
            520,
            620,
        )

        self.setModal(True)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            False,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent,
            True,
        )

        self.setAutoFillBackground(True)

        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {PALETTE.bg_primary};
                color: {PALETTE.text_primary};
            }}

            QLabel {{
                background-color: transparent;
            }}

            QLineEdit {{
                background-color: {PALETTE.bg_secondary};
                color: {PALETTE.text_primary};
                border: 1px solid {PALETTE.border};
                border-radius: 6px;
                padding: 10px;
                min-height: 22px;
            }}

            QLineEdit:focus {{
                border: 1px solid {PALETTE.accent};
            }}

            QPushButton {{
                background-color: {PALETTE.accent};
                color: {PALETTE.text_on_accent};
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                min-height: 22px;
            }}

            QPushButton:hover {{
                background-color: {PALETTE.accent_hover};
            }}

            QPushButton:pressed {{
                background-color: {PALETTE.accent};
            }}
            """
        )

        self._build_ui()

    # =============================================================
    # Build UI
    # =============================================================

    def _build_ui(self):
        root = QVBoxLayout(self)

        root.setContentsMargins(
            SPACING.xl,
            SPACING.xl,
            SPACING.xl,
            SPACING.xl,
        )

        root.setSpacing(
            SPACING.md
        )

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title = QLabel(
            "PulseMind"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setFont(
            Typography.h1()
        )

        title.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            background-color: transparent;
            """
        )

        root.addWidget(
            title
        )

        subtitle = QLabel(
            "ECG Analysis System"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        root.addWidget(
            subtitle
        )

        root.addSpacing(
            SPACING.lg
        )

        # ---------------------------------------------------------
        # Pages
        # ---------------------------------------------------------

        self.stack = QStackedWidget()

        self.stack.setStyleSheet(
            """
            QStackedWidget {
                background-color: transparent;
                border: none;
            }

            QWidget {
                background-color: transparent;
            }
            """
        )

        self.login_page = (
            self._build_login_page()
        )

        self.register_page = (
            self._build_register_page()
        )

        self.stack.addWidget(
            self.login_page
        )

        self.stack.addWidget(
            self.register_page
        )

        root.addWidget(
            self.stack,
            stretch=1,
        )

    # =============================================================
    # Login page
    # =============================================================

    def _build_login_page(self):
        page = QWidget()

        page.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        layout = QVBoxLayout(page)

        layout.setSpacing(
            SPACING.sm
        )

        heading = QLabel(
            "Welcome Back"
        )

        heading.setFont(
            Typography.h2()
        )

        heading.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            heading
        )

        description = QLabel(
            "Login to access PulseMind."
        )

        description.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            description
        )

        layout.addSpacing(
            SPACING.md
        )

        # Username

        username_label = QLabel(
            "Username"
        )

        username_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            username_label
        )

        self.login_username = QLineEdit()

        self.login_username.setPlaceholderText(
            "Enter your username"
        )

        layout.addWidget(
            self.login_username
        )

        # Password

        password_label = QLabel(
            "Password"
        )

        password_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            password_label
        )

        self.login_password = QLineEdit()

        self.login_password.setPlaceholderText(
            "Enter your password"
        )

        self.login_password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.login_password.returnPressed.connect(
            self.login
        )

        layout.addWidget(
            self.login_password
        )

        # Login message

        self.login_message = QLabel(
            ""
        )

        self.login_message.setWordWrap(
            True
        )

        self.login_message.setStyleSheet(
            f"""
            color: {PALETTE.danger};
            background-color: transparent;
            """
        )

        layout.addWidget(
            self.login_message
        )

        layout.addSpacing(
            SPACING.sm
        )

        # Login button

        login_button = QPushButton(
            "Login"
        )

        login_button.setMinimumHeight(
            42
        )

        login_button.clicked.connect(
            self.login
        )

        layout.addWidget(
            login_button
        )

        layout.addSpacing(
            SPACING.sm
        )

        # Registration

        register_layout = QHBoxLayout()

        register_label = QLabel(
            "Don't have an account?"
        )

        register_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        register_button = QPushButton(
            "Create Account"
        )

        register_button.setFlat(
            True
        )

        register_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {PALETTE.accent};
                border: none;
                padding: 4px;
            }}

            QPushButton:hover {{
                color: {PALETTE.text_primary};
                background-color: transparent;
            }}
            """
        )

        register_button.clicked.connect(
            self.show_register
        )

        register_layout.addStretch(
            1
        )

        register_layout.addWidget(
            register_label
        )

        register_layout.addWidget(
            register_button
        )

        register_layout.addStretch(
            1
        )

        layout.addLayout(
            register_layout
        )

        layout.addStretch(
            1
        )

        return page

    # =============================================================
    # Register page
    # =============================================================

    def _build_register_page(self):
        page = QWidget()

        page.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        layout = QVBoxLayout(page)

        layout.setSpacing(
            SPACING.sm
        )

        heading = QLabel(
            "Create Account"
        )

        heading.setFont(
            Typography.h2()
        )

        heading.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            heading
        )

        description = QLabel(
            "Create a local PulseMind account."
        )

        description.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            description
        )

        layout.addSpacing(
            SPACING.md
        )

        # Username

        username_label = QLabel(
            "Username"
        )

        username_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            username_label
        )

        self.register_username = QLineEdit()

        self.register_username.setPlaceholderText(
            "Choose a username"
        )

        layout.addWidget(
            self.register_username
        )

        # Password

        password_label = QLabel(
            "Password"
        )

        password_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            password_label
        )

        self.register_password = QLineEdit()

        self.register_password.setPlaceholderText(
            "Choose a password"
        )

        self.register_password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(
            self.register_password
        )

        # Confirm password

        confirm_label = QLabel(
            "Confirm Password"
        )

        confirm_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: transparent;
            """
        )

        layout.addWidget(
            confirm_label
        )

        self.register_confirm = QLineEdit()

        self.register_confirm.setPlaceholderText(
            "Enter password again"
        )

        self.register_confirm.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(
            self.register_confirm
        )

        # Message

        self.register_message = QLabel(
            ""
        )

        self.register_message.setWordWrap(
            True
        )

        self.register_message.setStyleSheet(
            """
            background-color: transparent;
            """
        )

        layout.addWidget(
            self.register_message
        )

        layout.addSpacing(
            SPACING.sm
        )

        # Register button

        register_button = QPushButton(
            "Create Account"
        )

        register_button.setMinimumHeight(
            42
        )

        register_button.clicked.connect(
            self.register
        )

        layout.addWidget(
            register_button
        )

        # Back button

        back_button = QPushButton(
            "Back to Login"
        )

        back_button.setFlat(
            True
        )

        back_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {PALETTE.accent};
                border: none;
                padding: 6px;
            }}

            QPushButton:hover {{
                color: {PALETTE.text_primary};
                background-color: transparent;
            }}
            """
        )

        back_button.clicked.connect(
            self.show_login
        )

        layout.addWidget(
            back_button
        )

        layout.addStretch(
            1
        )

        return page

    # =============================================================
    # Login
    # =============================================================

    def login(self):

        username = (
            self.login_username
            .text()
            .strip()
        )

        password = (
            self.login_password
            .text()
        )

        if not username:

            self.login_message.setText(
                "Please enter your username."
            )

            return

        if not password:

            self.login_message.setText(
                "Please enter your password."
            )

            return

        user = (
            database_manager
            .authenticate_user(
                username,
                password,
            )
        )

        if user is None:

            self.login_message.setText(
                "Incorrect username or password."
            )

            return

        self.user = user

        self.accept()

    # =============================================================
    # Registration
    # =============================================================

    def register(self):

        username = (
            self.register_username
            .text()
            .strip()
        )

        password = (
            self.register_password
            .text()
        )

        confirm_password = (
            self.register_confirm
            .text()
        )

        if password != confirm_password:

            self.register_message.setStyleSheet(
                f"""
                color: {PALETTE.danger};
                background-color: transparent;
                """
            )

            self.register_message.setText(
                "Passwords do not match."
            )

            return

        success, message = (
            database_manager
            .register_user(
                username,
                password,
            )
        )

        if not success:

            self.register_message.setStyleSheet(
                f"""
                color: {PALETTE.danger};
                background-color: transparent;
                """
            )

            self.register_message.setText(
                message
            )

            return

        self.register_message.setStyleSheet(
            f"""
            color: {PALETTE.success};
            background-color: transparent;
            """
        )

        self.register_message.setText(
            "Account created successfully. "
            "You can now login."
        )

        self.login_username.setText(
            username
        )

        self.login_password.clear()

        self.show_login()

    # =============================================================
    # Switch to registration
    # =============================================================

    def show_register(self):

        self.login_message.clear()

        self.stack.setCurrentWidget(
            self.register_page
        )

        self.register_username.setFocus()

    # =============================================================
    # Switch to login
    # =============================================================

    def show_login(self):

        self.register_message.clear()

        self.stack.setCurrentWidget(
            self.login_page
        )

        self.login_username.setFocus()