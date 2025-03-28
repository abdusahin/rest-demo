from alembic import op

revision: str = "1"
down_revision: str = None


def upgrade() -> None:
    op.execute(
        """
    CREATE TABLE insurance_quote (
    id SERIAL PRIMARY KEY,
    quote_amount NUMERIC(18,2) NOT NULL,
    quote_date TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    proposer VARCHAR(50) NOT NULL CHECK (LENGTH(proposer) <= 50 AND proposer <> ''),
    is_business_use BOOLEAN DEFAULT FALSE NOT NULL,
    vehicle_registration VARCHAR(10) NOT NULL CHECK (LENGTH(vehicle_registration) <= 10 AND vehicle_registration <> ''),
    agent_discount_amount NUMERIC(18,2) NULL,
    agent_notes VARCHAR(5000) NULL
);

        """
    )


def downgrade() -> None:
    op.execute(
        f"DROP TABLE insurance_quote"
    )
