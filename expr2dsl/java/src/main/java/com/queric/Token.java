package com.queric;

import java.util.Objects;

/**
 * Single token from the query string (AND, OR, NOT, TO, FIELD, WORD, PHRASE, punctuation).
 */
public final class Token {
    public enum Type {
        AND, OR, NOT, TO,
        FIELD, WORD, PHRASE,
        LPAR, RPAR, COLON, LBRACK, RBRACK,
        EOF
    }

    private final Type type;
    private final String value;

    public Token(Type type, String value) {
        this.type = type;
        this.value = value != null ? value : "";
    }

    public Type type() { return type; }
    public String value() { return value; }

    @Override
    public String toString() {
        return type + (value.isEmpty() ? "" : "(" + value + ")");
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Token token = (Token) o;
        return type == token.type && Objects.equals(value, token.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(type, value);
    }
}
