const SilenziaApp = (function() {
  
  
  const CONFIG = {
    API: {
      PRENOTAZIONI: '/api/prenotazioni',
      TIMEOUT: 5000 // ms
    },
    UI: {
      DURATA_MESSAGGI: 3000,
      FORMATO_DATA: 'DD-MM-YYYY'
    }
  };

  // Cache DOM - evita querySelectorAll continui
  const DOM = {
    form: document.getElementById('formPrenotazione'),
    listaPrenotazioni: document.getElementById('listaPrenotazioni'),
    idModifica: document.getElementById('editId'),
    btnInvia: document.getElementById('submitBtn'),
    boxMessaggio: document.getElementById("successMessage"),
    titoloLista: document.getElementById("titoloPrenotazioni")
  };

  // Utils 
  const Utils = {
    formattaData: data => data.split('-').reverse().join('-'),
    validaEmail: email => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email),
    scrollSu: () => window.scrollTo({ top: 0, behavior: 'smooth' })
  };

  // Gestione feedback utente
  class GestoreFeedback {
    static mostra(messaggio, errore = false) {
      Object.assign(DOM.boxMessaggio.style, {
        display: "block",
        backgroundColor: errore ? "#fee2e2" : "",
        color: errore ? "#991b1b" : ""
      });
      DOM.boxMessaggio.textContent = messaggio;

      // Pulizia automatica
      setTimeout(() => {
        DOM.boxMessaggio.style.display = "none";
      }, CONFIG.UI.DURATA_MESSAGGI);
    }
  }

  // API prenotazioni
  class APIPrenotazioni {
    static async gestisciRisposta(response) {
      const dati = await response.json();
      if (!response.ok) {
        // Formatta errore per l'utente
        const msg = dati.dettaglio || dati.errore || 'Ops, qualcosa è andato storto';
        throw new Error(msg);
      }
      return dati;
    }

    static async getPrenotazioni() {
      try {
        const response = await fetch(CONFIG.API.PRENOTAZIONI);
        return await this.gestisciRisposta(response);
      } catch (err) {
        throw new Error(`Errore caricamento prenotazioni: ${err.message}`);
      }
    }

    static async salvaPrenotazione(prenotazione, id = null) {
      const url = id ? `${CONFIG.API.PRENOTAZIONI}/${id}` : CONFIG.API.PRENOTAZIONI;
      try {
        const response = await fetch(url, {
          method: id ? 'PUT' : 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(prenotazione)
        });
        return await this.gestisciRisposta(response);
      } catch (err) {
        throw new Error(`Errore salvataggio: ${err.message}`);
      }
    }

    static async cancellaPrenotazione(id) {
      try {
        const response = await fetch(`${CONFIG.API.PRENOTAZIONI}/${id}`, { 
          method: 'DELETE' 
        });
        return await this.gestisciRisposta(response);
      } catch (err) {
        throw new Error(`Errore cancellazione: ${err.message}`);
      }
    }
  }

  // Gestione UI
  class GestoreUI {
    static renderPrenotazione(prenotazione) {
      return `
        <div class="card">
          <div class="prenotazione-dettagli">
            <p>👤Nome: ${prenotazione.nome} ${prenotazione.cognome}</p>
            <p>📧Email: ${prenotazione.email}</p>
            <p>📅Data: ${Utils.formattaData(prenotazione.data)}</p>
            <p>⌚Ora: ${prenotazione.ora}</p>
            <p>👥Persone: ${prenotazione.persone}</p>
            <p>🎫Codice: ${prenotazione.codice}</p>
            <p class="text-muted"><small>Usa la password del tuo account con il codice per accedere</small></p>
          </div>
          <div class="actions">
            <button onclick='SilenziaApp.modificaPrenotazione(${JSON.stringify(prenotazione)})'>Modifica</button>
            <button onclick="SilenziaApp.cancellaPrenotazione('${prenotazione._id}')">Elimina</button>
          </div>
        </div>
      `;
    }

    static renderPrenotazioni(prenotazioni = []) {
      DOM.titoloLista.style.display = prenotazioni.length ? 'block' : 'none';
      DOM.listaPrenotazioni.innerHTML = prenotazioni.length
        ? prenotazioni
            .sort((a, b) => new Date(`${a.data}T${a.ora}`) - new Date(`${b.data}T${b.ora}`))
            .map(this.renderPrenotazione)
            .join('')
        : '<p class="no-prenotazioni">Non hai prenotazioni attive.</p>';
    }

    static pulisciForm() {
      DOM.form.reset();
      DOM.idModifica.value = '';
      DOM.btnInvia.textContent = "Prenota";
      DOM.btnInvia.style.background = "";
    }
  }

  // Controller principale
  class Controller {
    constructor() {
      this.init();
      this.caricaPrenotazioni();
    }

    init() {
      // Setup validazione data/ora
      const oggi = new Date();
      const inputData = document.getElementById('data');
      const inputOra = document.getElementById('ora');
      
      if (inputData) {
        inputData.min = oggi.toISOString().split('T')[0];
        inputData.max = `${oggi.getFullYear()}-12-31`;
        
        // Check orario se prenota oggi
        inputData.addEventListener('change', () => {
          const dataScelta = new Date(inputData.value);
          const oraAttuale = new Date();
          
          if (dataScelta.toDateString() === oraAttuale.toDateString()) {
            const options = inputOra.options;
            const oraCorrente = oraAttuale.getHours();
            
            // Disabilita orari passati
            for (let i = 0; i < options.length; i++) {
              const oraOpzione = parseInt(options[i].value);
              options[i].disabled = oraOpzione <= oraCorrente;
            }
          } else {
            // Riabilita tutti gli orari
            for (let i = 0; i < inputOra.options.length; i++) {
              inputOra.options[i].disabled = false;
            }
          }
        });
      }
      
      // Event binding
      DOM.form?.addEventListener('submit', this.gestisciSubmit.bind(this));
    }

    async gestisciSubmit(e) {
      e.preventDefault();
      DOM.btnInvia.disabled = true;

      try {
        if (!Utils.validaEmail(DOM.form.email.value)) {
          throw new Error("Email non valida");
        }

        const prenotazione = Object.fromEntries(
          ['nome', 'cognome', 'email', 'data', 'ora', 'persone']
          .map(id => [id, document.getElementById(id).value])
        );

        const idModifica = DOM.idModifica.value;
        await APIPrenotazioni.salvaPrenotazione(prenotazione, idModifica);
        
        GestoreUI.pulisciForm();
        await this.caricaPrenotazioni();
        GestoreFeedback.mostra(
          idModifica ? "Modifiche salvate!" : "Prenotazione confermata!"
        );
      } catch (err) {
        GestoreFeedback.mostra(err.message, true);
      } finally {
        DOM.btnInvia.disabled = false;
      }
    }

    async caricaPrenotazioni() {
      try {
        const { prenotazioni } = await APIPrenotazioni.getPrenotazioni();
        GestoreUI.renderPrenotazioni(prenotazioni);
      } catch (err) {
        DOM.listaPrenotazioni.innerHTML = `<p class="error-message">Errore: ${err.message}</p>`;
      }
    }
  }

  // Istanza controller
  const controller = new Controller();

  // API pubblica
  return {
    modificaPrenotazione: function(prenotazione) {
      Object.entries(prenotazione).forEach(([key, value]) => {
        const elemento = document.getElementById(key);
        if (elemento && key !== '_id') elemento.value = value;
      });
      DOM.idModifica.value = prenotazione._id;
      DOM.btnInvia.textContent = "Conferma";
      DOM.btnInvia.style.background = "var(--colore-primario)";
      Utils.scrollSu();
      document.getElementById('nome')?.focus();
    },

    cancellaPrenotazione: async function(id) {
      if (!confirm("Vuoi davvero cancellare questa prenotazione?")) return;
      try {
        await APIPrenotazioni.cancellaPrenotazione(id);
        await controller.caricaPrenotazioni();
        GestoreFeedback.mostra("Prenotazione cancellata!");
      } catch (err) {
        GestoreFeedback.mostra(err.message, true);
      }
    }
  };
})();

// Espone app globalmente
window.SilenziaApp = SilenziaApp;
