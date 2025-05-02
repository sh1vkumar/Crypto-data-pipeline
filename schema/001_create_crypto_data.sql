DROP TABLE IF EXISTS crypto_data;

CREATE TABLE crypto_data (
    id TEXT PRIMARY KEY,
    symbol TEXT NOT NULL CHECK (symbol = LOWER(symbol)),
    name TEXT NOT NULL,
    image TEXT,
    
    current_price NUMERIC,
    market_cap BIGINT,
    market_cap_rank INTEGER,
    fully_diluted_valuation BIGINT,
    total_volume BIGINT,

    high_24h NUMERIC,
    low_24h NUMERIC,
    price_change_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    market_cap_change_24h BIGINT,
    market_cap_change_percentage_24h NUMERIC,

    circulating_supply NUMERIC,
    total_supply NUMERIC,
    max_supply NUMERIC,

    ath NUMERIC,
    ath_change_percentage NUMERIC,
    ath_date TIMESTAMPTZ,

    atl NUMERIC,
    atl_change_percentage NUMERIC,
    atl_date TIMESTAMPTZ,

    roi JSONB,  -- optionally normalize later
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);