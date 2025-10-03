import streamlit as st

def add_persistent_toast(message, icon="ℹ️", duration=None):
    """
    Ajoute un toast qui persistera après un rerun
    
    Args:
        message (str): Le message à afficher
        icon (str): L'icône du toast (emoji)
        duration (str): 'short' ou 'long', None pour durée par défaut
    """
    if 'pending_toasts' not in st.session_state:
        st.session_state.pending_toasts = []
    
    st.session_state.pending_toasts.append({
        'message': message,
        'icon': icon,
        'duration': duration
    })

def display_pending_toasts():
    """
    Affiche tous les toasts en attente et les nettoie
    Cette fonction doit être appelée au début de main_app()
    """
    if 'pending_toasts' in st.session_state and st.session_state.pending_toasts:
        for toast_data in st.session_state.pending_toasts:
            if toast_data['duration']:
                st.toast(
                    toast_data['message'],
                    icon=toast_data['icon'],
                    duration=toast_data['duration']
                )
            else:
                st.toast(
                    toast_data['message'],
                    icon=toast_data['icon']
                )
        
        # Nettoyer les toasts affichés
        st.session_state.pending_toasts = []