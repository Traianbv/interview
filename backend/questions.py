questions = [
    {
        "question": "Cum investighezi o alertă de Brute Force?",
        "level": "SOC1",
        "keywords": ["loguri", "autentificare", "ip", "tentative", "blocare", "analiză", "investigare"],
        "answer": "Pentru investigarea unei alerte de Brute Force, urmez următorii pași: 1) Analizez logurile de autentificare pentru a identifica IP-ul sursă și numărul de tentative eșuate, 2) Verific dacă IP-ul este cunoscut ca fiind malitios, 3) Examinez tiparul încercărilor (username-uri încercate, frecvență), 4) Verific dacă conturile vizate au fost compromise, 5) Recomand blocarea IP-ului și resetarea parolelor pentru conturile vizate.",
        "follow_up": {
            "question": "Ce tipuri de loguri ai analiza pentru un atac Brute Force pe un server Windows?",
            "keywords": ["security log", "event id", "4625", "autentificare eșuată", "windows logs"],
            "answer": "Pentru un server Windows, analizez în special Security Log-urile, concentrându-mă pe Event ID 4625 (Autentificare eșuată). Aceste loguri conțin informații importante precum: IP-ul sursă, username-ul încercat, timestamp-ul, tipul de autentificare și codul de eroare. De asemenea, verific și Event ID 4624 pentru autentificări reușite suspecte și Event ID 4776 pentru încercări de autentificare NTLM."
        }
    },
    {
        "question": "Ce este un SIEM și cum îl folosești în SOC?",
        "level": "SOC1",
        "keywords": ["securitate", "monitorizare", "evenimente", "loguri", "corelație", "alertă", "investigare"],
        "answer": "Un SIEM (Security Information and Event Management) este o platformă care colectează, corelează și analizează logurile și evenimentele de securitate din întreaga infrastructură. În SOC, folosim SIEM-ul pentru: 1) Agregarea centralizată a logurilor, 2) Detectarea anomaliilor și a amenințărilor prin corelarea evenimentelor, 3) Generarea de alerte pentru activități suspecte, 4) Investigarea incidentelor folosind căutări avansate în loguri, 5) Raportarea și conformitatea.",
        "follow_up": {
            "question": "Cum configurezi reguli de corelare în SIEM pentru a detecta un atac de tip Brute Force?",
            "keywords": ["reguli", "corelare", "threshold", "time window", "ip source", "failed login"],
            "answer": "Pentru a detecta Brute Force în SIEM, configurez reguli de corelare care: 1) Monitorizează evenimentele de autentificare eșuată (ex: Event ID 4625) într-o fereastră de timp specifică (ex: 5 minute), 2) Agregă încercările după IP sursă, 3) Setez un threshold (ex: 5 încercări eșuate) care declanșează alerta, 4) Exclud IP-uri cunoscute ca fiind sigure (whitelist), 5) Adaug context suplimentar precum geolocația IP-ului și istoricul său."
        }
    },
    {
        "question": "Cum diferențiezi între un fals pozitiv și o amenințare reală?",
        "level": "SOC1",
        "keywords": ["analiză", "context", "verificare", "ip", "comportament", "istoric", "evaluare"],
        "answer": "Diferențierea se face prin: 1) Analiza contextului complet (ce activități precedă și urmează alertelor), 2) Verificarea reputației IP-urilor și domeniilor implicate, 3) Examinarea comportamentului utilizatorului/ sistemului (dacă se abate de la normal), 4) Consultarea istoricului de alerte similare, 5) Evaluarea impactului potențial.",
        "follow_up": {
            "question": "Ce instrumente folosești pentru a verifica reputația unui IP suspect?",
            "keywords": ["whois", "dns", "blacklist", "geolocation", "threat intelligence"],
            "answer": "Pentru verificarea reputației unui IP folosesc mai multe instrumente: 1) WHOIS pentru informații despre registrant, 2) DNS lookups pentru a vedea domeniile asociate, 3) Verificare în multiple blacklist-uri (Spamhaus, AbuseIPDB), 4) Servicii de geolocație pentru a identifica originea, 5) Platforme de threat intelligence (VirusTotal, AlienVault OTX) pentru a vedea istoricul de activități malitioase."
        }
    },
    {
        "question": "Ce este un IDS/IPS și cum îl configurezi?",
        "level": "SOC1",
        "keywords": ["detectare", "prevenire", "intruziune", "reguli", "semnături", "monitorizare", "configurare"],
        "answer": "Un IDS (Intrusion Detection System) monitorizează traficul pentru activități suspecte, iar un IPS (Intrusion Prevention System) poate și bloca aceste activități. Configurarea implică: 1) Definirea politicilor de securitate, 2) Activarea regulilor relevante pentru mediul protejat, 3) Setarea threshold-urilor pentru alertă, 4) Configurarea excluderilor pentru trafic legitim, 5) Integrarea cu alte sisteme de securitate.",
        "follow_up": {
            "question": "Cum optimizezi regulile IDS/IPS pentru a reduce falsurile pozitive?",
            "keywords": ["tuning", "threshold", "whitelist", "baseline", "fals pozitiv"],
            "answer": "Optimizarea regulilor IDS/IPS se face prin: 1) Crearea unei baseline a traficului normal, 2) Ajustarea threshold-urilor bazată pe activitatea reală, 3) Implementarea whitelist-urilor pentru IP-uri și servicii de încredere, 4) Dezactivarea regulilor care nu sunt relevante pentru mediul specific, 5) Monitorizarea continuă și ajustarea regulilor bazată pe feedback-ul din investigații."
        }
    },
    {
        "question": "Cum gestionezi un incident de securitate?",
        "level": "SOC1",
        "keywords": ["procedură", "răspuns", "conținere", "eradicare", "recuperare", "raportare", "lecții"],
        "answer": "Gestionarea unui incident implică: 1) Identificarea și clasificarea incidentului, 2) Conținerea imediată a amenințării, 3) Investigarea pentru a înțelege amploarea, 4) Eradicarea cauzei rădăcină, 5) Recuperarea sistemelor afectate, 6) Documentarea și raportarea incidentului, 7) Învățarea lecțiilor pentru îmbunătățirea proceselor.",
        "follow_up": {
            "question": "Ce informații includi în raportul post-incident?",
            "keywords": ["timeline", "impact", "rădăcină", "recomandări", "documentație"],
            "answer": "Raportul post-incident trebuie să includă: 1) Timeline detaliat al incidentului, 2) Descrierea tehnică a atacului și vectorilor de infecție, 3) Analiza impactului asupra business-ului, 4) Identificarea cauzei rădăcină, 5) Pașii de remediere luați, 6) Recomandări pentru prevenirea incidentelor similare, 7) Lecții învățate și îmbunătățiri propuse pentru procesele de securitate."
        }
    },
    {
        "question": "Cum diferențiezi un incident real de un fals pozitiv într-un SIEM?",
        "level": "SOC2",
        "keywords": ["context", "corelare", "intel", "indicatori", "analiză"],
        "answer": "Prin corelarea alertelor cu alte surse de date, folosirea inteligenței despre amenințări și verificarea contextului rețelei și sistemului afectat."
    },
    {
        "question": "Cum folosești MITRE ATT&CK într-o investigație?",
        "level": "SOC2",
        "keywords": ["tactică", "tehnică", "corelare", "identificare", "măsuri"],
        "answer": "Mapez activitatea atacatorului la tehnicile din MITRE ATT&CK, pentru a înțelege fazele atacului și a lua contramăsuri."
    },
    {
        "question": "Ce faci dacă observi trafic exfiltrare de date criptat către o țară suspectă?",
        "level": "SOC2",
        "keywords": ["trafic", "criptat", "geolocație", "firewall", "containment"],
        "answer": "Izolez sistemul afectat, analizez pachetele suspecte, identific aplicația responsabilă și raportez incidentul pentru acțiune."
    },
    {
        "question": "Ce este un firewall și ce rol are într-un SOC?",
        "level": "SOC1",
        "keywords": ["firewall", "perimetru", "filtrare", "pachete", "politici"],
        "answer": "Un firewall monitorizează și controlează traficul de rețea pe baza politicilor de securitate definite. În SOC este folosit pentru a preveni accesul neautorizat, a proteja resursele critice și a genera alerte pentru traficul suspect."
    },
    {
        "question": "Explică modelul Kill Chain și cum îl aplici în gestionarea incidentelor.",
        "level": "SOC1",
        "keywords": ["kill chain", "reconnaissance", "weaponization", "delivery", "exploitation", "installation", "command and control"],
        "answer": "Modelul Kill Chain descrie fazele unui atac: Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command and Control și Actions on Objectives. În SOC, folosim acest model pentru a identifica faza atacului și a implementa contramăsuri adecvate fiecărei etape."
    },
    {
        "question": "Cum configurezi un honeypot pentru monitorizarea activității rău-intenționate?",
        "level": "SOC1",
        "keywords": ["honeypot", "capcană", "monitorizare", "loguri", "alertă"],
        "answer": "Un honeypot este un sistem decoy configurat să pară vulnerabil. Configurarea implică: 1) Standalone sau în DMZ, 2) Logarea completă a traficului, 3) Detectarea și alertarea accesului neautorizat, 4) Analiza pentru a înțelege tehnicile atacatorilor și pentru a îmbunătăți apărarea."
    },
    {
        "question": "Cum performezi analiza traficului de rețea (pcap) pentru investigații?",
        "level": "SOC2",
        "keywords": ["pcap", "Wireshark", "filtrare", "protocol", "anomalie"],
        "answer": "Captur traficul de rețea folosind tcpdump, analizez fișierul pcap în Wireshark cu filtre pentru sursă, destinație și protocoale. Caut anomalii precum sesiuni neobișnuite, retransmisii și pachete criptate suspecte."
    },
    {
        "question": "Cum dezvolți o regulă de detectare bazată pe Machine Learning în SIEM?",
        "level": "SOC2",
        "keywords": ["machine learning", "anomalie", "model", "antrenare", "prag"],
        "answer": "Identific caracteristici relevante din loguri, antrenez un model (ex: clustering pentru anomalie), import regula ML în SIEM, monitorez alertele generate și ajustez pragurile pentru a reduce falsurile."
    },
    {
        "question": "Cum integrezi fluxuri de Threat Intelligence (feed-uri) într-un workflow SOC?",
        "level": "SOC2",
        "keywords": ["threat intelligence", "feed", "IOC", "STIX", "TAXII"],
        "answer": "Configurez SIEM să fie client TAXII/STIX, import date IOC din feed-uri, corelez aceste IOC cu logurile existente, generez alerte automate și actualizez regulile de detecție pe baza acestor date."
    },
    # Întrebări practice simple
    {
        "question": "Scrie o comandă care afișează cele mai consumatoare 5 procese după memorie și explică fiecare pas al comenzii.",
        "level": "SOC1",
        "keywords": ["ps", "memorie", "procese", "head", "explicație"],
        "answer": "Comandă: `ps aux --sort=-%mem | head -n 6`\n- `ps aux` listează toate procesele cu detalii.\n- `--sort=-%mem` sortează procesele descrescător după consumul de memorie.\n- `head -n 6` afișează primele 6 linii (header + top 5 procese)."
    },
    {
        "question": "Comanda folosita pentru a urmări în timp real logul de autentificare.",
        "level": "SOC1",
        "keywords": ["tail", "auth.log", "monitorizare", "autentificare"],
        "answer": "Folosește `tail -f /var/log/auth.log` pentru a vizualiza intrările de autentificare pe măsură ce apar."
    },
    {
        "question": "Listă toate conexiunile SSH active folosind netstat.",
        "level": "SOC2",
        "keywords": ["netstat", "SSH", "conexiuni", "22"],
        "answer": "Folosește `netstat -tn | grep ':22'` pentru a vedea conexiunile active pe portul 22."
    },
    {
        "question": "Blochează IP-ul 203.0.113.5 folosind iptables.",
        "level": "SOC2",
        "keywords": ["iptables", "DROP", "IP", "firewall"],
        "answer": "Folosește `iptables -A INPUT -s 203.0.113.5 -j DROP` pentru a bloca traficul provenit de la acest IP."
    },
    {
        "question": "Ce este subnetting și cum împarți o rețea în subrețele?",
        "level": "NETADMIN",
        "keywords": ["subnetting", "mască de rețea", "CIDR", "prefix"],
        "answer": "Subnetting-ul implică împărțirea unei rețele mari în subrețele mai mici folosind o mască de rețea. Prin modificarea prefixului CIDR se pot genera adrese de rețea unice pentru fiecare subrețea."
    },
    {
        "question": "Care este diferența dintre un switch și un router?",
        "level": "NETADMIN",
        "keywords": ["switch", "router", "layer2", "layer3"],
        "answer": "Un switch operează la layer 2 și transmite pachetele în baza adreselor MAC, în timp ce un router operează la layer 3 și direcționează traficul între rețele folosind adrese IP."
    },
    {
        "question": "Ce rol are protocolul DHCP într-o rețea și cum funcționează?",
        "level": "NETADMIN",
        "keywords": ["DHCP", "IP", "leasing", "client", "server"],
        "answer": "DHCP (Dynamic Host Configuration Protocol) alocă dinamic adrese IP și alte setări de rețea (gateway, DNS) clienților. Clientul trimite o cerere (DHCP Discover), serverul oferă un IP (DHCP Offer), clientul acceptă (DHCP Request) iar serverul confirmă (DHCP Ack)."
    },
    {
        "question": "Cum funcționează protocolul ARP și de ce este important?",
        "level": "NETADMIN",
        "keywords": ["ARP", "adresă MAC", "mapping", "broadcast"],
        "answer": "ARP (Address Resolution Protocol) traduce adrese IP în adrese MAC în rețelele Ethernet. Trimite broadcast pentru a afla MAC-ul asociat unei adrese IP și stochează rezultatele în cache pentru eficiență."
    },
    {
        "question": "Ce este NAT și când îl folosești?",
        "level": "NETADMIN",
        "keywords": ["NAT", "mascare de adrese", "public", "privat"],
        "answer": "NAT (Network Address Translation) permite tradusul adreselor private în adrese publice pentru trafic Internet. Este folosit în rețele locale pentru a economisi adrese publice și a securiza topologia internă."
    },
    {
        "question": "Cum îmbunătățești securitatea într-o rețea wireless?",
        "level": "NETADMIN",
        "keywords": ["WPA2", "WPA3", "SSID", "criptare", "autentificare"],
        "answer": "Pentru securitate wireless se folosesc standarde WPA2/WPA3, criptare AES, autentificare robustă (802.1X), schimbarea SSID implicite și implementarea unui VLAN separat pentru guest."
    },
    {
        "question": "Ce este VLAN și cum îl configurezi pe un switch gestionabil?",
        "level": "NETADMIN",
        "keywords": ["VLAN", "switch", "trunk", "access port"],
        "answer": "VLAN (Virtual LAN) segregă traficul în rețele logice separate. Pe un switch gestionabil configurezi porturile ca access (un singur VLAN) sau trunk (mai multe VLAN-uri) și setezi ID-ul VLAN corespunzător."
    },
    {
        "question": "Cum diagnostichezi probleme de conectivitate folosind comenzi CLI?",
        "level": "NETADMIN",
        "keywords": ["ping", "traceroute", "netstat", "ifconfig", "ipconfig"],
        "answer": "Folosesc `ping` pentru a verifica conectivitatea de bază, `traceroute` pentru a investiga ruta pachetelor, `ifconfig`/`ipconfig` pentru starea interfețelor și `netstat` pentru conexiuni active."
    },
    {
        "question": "Ce este BGP și când ai nevoie de el?",
        "level": "NETADMIN",
        "keywords": ["BGP", "AS", "routing", "internet", "protocol"],
        "answer": "BGP (Border Gateway Protocol) este protocol de rutare externă între AS-uri pe Internet. Este esențial pentru ISP-uri și organizații cu multiple legături ISP pentru a gestiona rutele și politicile de trafic."
    },
    {
        "question": "Cum configurezi QoS pentru a prioritiza traficul VoIP?",
        "level": "NETADMIN",
        "keywords": ["QoS", "VoIP", "prioritizare", "coșuri", "bandwidth"],
        "answer": "Configurez QoS prin clasificare (marking) a pachetelor VoIP, alocare de cozi prioritare și limitări de bandwidth pentru traficul non-prioritar pentru a asigura calitatea apelurilor."
    },
    # Întrebări SOFTWAREDEV
    {
        "question": "Explică diferența dintre o listă și un tuple în Python?",
        "level": "SOFTWAREDEV",
        "keywords": ["list", "tuple", "mutable", "immutable"],
        "answer": "O listă este mutable (poate fi modificată după creare), în timp ce un tuple este imutabil (nu poate fi modificat). Tuple-urile sunt mai rapide și pot fi folosite ca chei în dict."
    },
    {
        "question": "Ce este programarea orientată pe obiecte (OOP) și care sunt cele patru principii de bază?",
        "level": "SOFTWAREDEV",
        "keywords": ["OOP", "encapsulation", "inheritance", "polymorphism", "abstraction"],
        "answer": "OOP este un stil de programare bazat pe obiecte. Principiile de bază sunt: encapsularea, moștenirea, polimorfismul și abstractizarea."
    },
    {
        "question": "Ce este un RESTful API și care sunt principiile sale?",
        "level": "SOFTWAREDEV",
        "keywords": ["REST", "API", "stateless", "endpoint", "CRUD"],
        "answer": "Un RESTful API respectă principiul stateless, folosește URL-uri pentru resurse și metode HTTP (GET, POST, PUT, DELETE) pentru operații CRUD."
    },
    {
        "question": "Cum funcționează tranzacțiile în bazele de date relaționale?",
        "level": "SOFTWAREDEV",
        "keywords": ["transaction", "ACID", "commit", "rollback"],
        "answer": "Tranzacțiile garantează proprietățile ACID: atomicitate, consistență, izolare și durabilitate. Se folosește COMMIT pentru salvare și ROLLBACK pentru anulare."
    },
    {
        "question": "Ce este un deadlock și cum îl previi?",
        "level": "SOFTWAREDEV",
        "keywords": ["deadlock", "lock", "concurrency", "prevention"],
        "answer": "Un deadlock apare când două sau mai multe procese se blochează reciproc așteptând resurse. Se previne prin strategie de evitare a cererilor circulare sau folosind timeout-uri."
    },
    {
        "question": "Explică modelul MVC?",
        "level": "SOFTWAREDEV",
        "keywords": ["MVC", "model", "view", "controller"],
        "answer": "Model-View-Controller separă datele (model), interfața (view) și logica (controller) pentru a îmbunătăți structura și mentenabilitatea aplicațiilor."
    },
    {
        "question": "Ce este garbage collection și cum funcționează în limbaje precum Python sau Java?",
        "level": "SOFTWAREDEV",
        "keywords": ["garbage collector", "memory management", "reference counting", "heap"],
        "answer": "Garbage collection eliberează memoria neutilizată automat. Python folosește reference counting și cycle detector, Java folosește mark-and-sweep și generational GC."
    },
    {
        "question": "Ce sunt design patterns și menționează trei exemple comune?",
        "level": "SOFTWAREDEV",
        "keywords": ["design patterns", "singleton", "factory", "observer"],
        "answer": "Design patterns sunt soluții reutilizabile la probleme recurente de design. Exemple: Singleton, Factory, Observer."
    },
    {
        "question": "Cum optimizezi performanța unei aplicații web?",
        "level": "SOFTWAREDEV",
        "keywords": ["caching", "load balancing", "CDN", "profiling"],
        "answer": "Optimizarea include caching la nivel de client și server, folosirea CDN, echilibrarea încărcării și profiling-ul codului pentru identificarea blocajelor."
    }
]  