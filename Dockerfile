FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo '#!/bin/bash' > /usr/local/bin/script.sh && \
    echo 'python setup.py' >> /usr/local/bin/script.sh && \
    echo 'python main.py' >> /usr/local/bin/script.sh && \
    chmod +x /usr/local/bin/script.sh
# Exécuter le script lors du démarrage du conteneur
CMD ["/usr/local/bin/script.sh"]