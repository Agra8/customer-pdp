FROM odoo:18.0

# Install library Python tambahan
USER root

# Install dependencies tambahan
RUN apt-get update && apt-get install -y \
    nano \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/odoo-venv
# Copy file requirements.txt dan install library tambahan
COPY requirements.txt /tmp/requirements.txt
RUN /opt/odoo-venv/bin/pip install --upgrade pip \
    && /opt/odoo-venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Pastikan Odoo menggunakan environment yang benar
ENV PATH="/opt/odoo-venv/bin:$PATH"

# Ganti kembali ke user Odoo
USER odoo

# Jalankan Odoo
CMD ["odoo"]