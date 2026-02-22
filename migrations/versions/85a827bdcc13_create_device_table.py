"""create device table

Revision ID: 85a827bdcc13
Revises: 
Create Date: 2026-02-21 13:17:41.678356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85a827bdcc13'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
                -- =========================
                -- GATEWAY
                -- =========================
                CREATE TABLE IF NOT EXISTS gateway (
                    id SERIAL PRIMARY KEY,
                    imei VARCHAR(50) NOT NULL UNIQUE,
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
               -- =========================
                -- RAW_MQTT_EVENT
                -- =========================
                CREATE TABLE IF NOT EXISTS raw_mqtt_event (
                    id SERIAL PRIMARY KEY,
                    gateway_id INTEGER REFERENCES gateway(id) ON DELETE SET NULL,
                    topic VARCHAR(255) NOT NULL,
                    payload_text TEXT NOT NULL,
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_raw_mqtt_gateway_received
                ON raw_mqtt_event (gateway_id, received_at DESC);
               
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
