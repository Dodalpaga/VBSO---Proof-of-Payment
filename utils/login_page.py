import streamlit as st
import time

def login_page():
    st.title("🔒 Connexion")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form(key="login_form"):
            username = st.text_input("Nom d'utilisateur", key="username")
            password = st.text_input("Mot de passe", type="password", key="password")
            submit_button = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
            
            if submit_button:
                try:
                    # Check if secrets and credentials are properly configured
                    if not hasattr(st, 'secrets'):
                        st.toast(
                            "Erreur : Aucun secret n'est configuré.",
                            icon="❌",
                            duration="long"
                        )
                        st.info("💡 Créez un fichier '.streamlit/secrets.toml' dans le répertoire du projet avec la structure suivante :")
                        st.markdown("""
                        ```toml
                        [credentials]
                        username = "your_username"
                        password = "your_password"
                        ```
                        """)
                        st.stop()
                    
                    if not hasattr(st.secrets, 'credentials'):
                        st.toast(
                            "Erreur : La section 'credentials' n'est pas trouvée dans secrets.toml.",
                            icon="❌",
                            duration="long"
                        )
                        st.info("💡 Assurez-vous que secrets.toml contient une section [credentials] avec 'username' et 'password'.")
                        st.markdown("""
                        ```toml
                        [credentials]
                        username = "your_username"
                        password = "your_password"
                        ```
                        """)
                        st.stop()
                    
                    if not (hasattr(st.secrets.credentials, 'username') and hasattr(st.secrets.credentials, 'password')):
                        st.toast(
                            "Erreur : Les champs 'username' et/ou 'password' sont manquants dans la section [credentials].",
                            icon="❌",
                            duration="long"
                        )
                        st.info("💡 Vérifiez que 'username' et 'password' sont définis sous [credentials] dans secrets.toml.")
                        st.markdown("""
                        ```toml
                        [credentials]
                        username = "your_username"
                        password = "your_password"
                        ```
                        """)
                        st.stop()
                    
                    # Verify credentials
                    if (username == st.secrets.credentials.username and 
                        password == st.secrets.credentials.password):
                        st.session_state.authenticated = True
                        st.toast("✅ Connexion réussie !")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.toast(
                            "Nom d'utilisateur ou mot de passe incorrect.",
                            icon="❌",
                            duration="long"
                        )
                except Exception as e:
                    st.toast(
                        f"Erreur inattendue lors de la connexion : {e}",
                        icon="❌",
                        duration="long"
                    )
                    st.info("💡 Vérifiez que le fichier '.streamlit/secrets.toml' est correctement configuré dans le répertoire du projet.")