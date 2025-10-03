import streamlit as st
import time
from utils.toast_manager import add_persistent_toast, display_pending_toasts

def login_page():
    
    # Display any pending toasts
    display_pending_toasts()
    
    # Set page title and layout
    c1, c2 = st.columns([1,10])
    
    with c1:
        # Display logo
        try:
            st.image("img/Logo VBSO.png")
        except FileNotFoundError:
            add_persistent_toast(
                "Erreur : Le fichier 'img/Logo VBSO.png' est introuvable.",
                icon="❌",
                duration="long"
            )
            return
    with c2:
        st.title("🔒 Connexion | Système de Gestion de Factures")
        st.markdown("---")
    # Create a centered container for the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### Se connecter")
            with st.form(key="login_form"):
                # Input fields with placeholders and help text
                username = st.text_input(
                    "Nom d'utilisateur",
                    placeholder="Entrez votre nom d'utilisateur",
                    key="username",
                    help="Saisissez le nom d'utilisateur défini dans secrets.toml"
                )
                password = st.text_input(
                    "Mot de passe",
                    type="password",
                    placeholder="Entrez votre mot de passe",
                    key="password",
                    help="Saisissez le mot de passe défini dans secrets.toml"
                )
                submit_button = st.form_submit_button(
                    "Se connecter 🚀",
                    type="primary",
                    use_container_width=True
                )
                
                if submit_button:
                    with st.spinner("Vérification des identifiants..."):
                        time.sleep(1)  # Simulate processing time
                        try:
                            # Check if secrets and credentials are properly configured
                            if not hasattr(st, 'secrets'):
                                add_persistent_toast(
                                    "Erreur : Aucun secret n'est configuré.",
                                    icon="❌",
                                    duration="long"
                                )
                                st.info(
                                    "💡 Créez un fichier '.streamlit/secrets.toml' dans le répertoire du projet avec la structure suivante :"
                                )
                                st.markdown(
                                    """
                                    ```toml
                                    [credentials]
                                    username = "your_username"
                                    password = "your_password"
                                    ```
                                    """
                                )
                                return
                            
                            if not hasattr(st.secrets, 'credentials'):
                                add_persistent_toast(
                                    "Erreur : La section 'credentials' n'est pas trouvée dans secrets.toml.",
                                    icon="❌",
                                    duration="long"
                                )
                                st.info(
                                    "💡 Assurez-vous que secrets.toml contient une section [credentials] avec 'username' et 'password'."
                                )
                                st.markdown(
                                    """
                                    ```toml
                                    [credentials]
                                    username = "your_username"
                                    password = "your_password"
                                    ```
                                    """
                                )
                                return
                            
                            if not (hasattr(st.secrets.credentials, 'username') and hasattr(st.secrets.credentials, 'password')):
                                add_persistent_toast(
                                    "Erreur : Les champs 'username' et/ou 'password' sont manquants dans la section [credentials].",
                                    icon="❌",
                                    duration="long"
                                )
                                st.info(
                                    "💡 Vérifiez que 'username' et 'password' sont définis sous [credentials] dans secrets.toml."
                                )
                                st.markdown(
                                    """
                                    ```toml
                                    [credentials]
                                    username = "your_username"
                                    password = "your_password"
                                    ```
                                    """
                                )
                                return
                            
                            # Verify credentials
                            if (username == st.secrets.credentials.username and 
                                password == st.secrets.credentials.password):
                                st.session_state.authenticated = True
                                add_persistent_toast(
                                    "✅ Connexion réussie ! Bienvenue !",
                                    icon="🎉",
                                    duration="long"
                                )
                                st.balloons()  # Celebratory animation
                                time.sleep(1)  # Brief pause for effect
                                st.rerun()
                            else:
                                add_persistent_toast(
                                    "Nom d'utilisateur ou mot de passe incorrect.",
                                    icon="❌",
                                    duration="long"
                                )
                        except Exception as e:
                            add_persistent_toast(
                                f"Erreur inattendue lors de la connexion : {e}",
                                icon="❌",
                                duration="long"
                            )
                            st.info(
                                "💡 Vérifiez que le fichier '.streamlit/secrets.toml' est correctement configuré dans le répertoire du projet."
                            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>© VBSO - 2025</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    login_page()