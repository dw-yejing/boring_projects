package com.queric;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.queric.Token.Type.*;

/**
 * Tokenizes the query string: AND, OR, NOT, TO, FIELD (only when followed by :), WORD, PHRASE, punctuation.
 */
public final class Lexer {
    private static final Pattern P_FIELD = Pattern.compile("[A-Za-z_][A-Za-z0-9_]*(?=\\s*:)");
    private static final Pattern P_WORD = Pattern.compile("[^\\s()\":\\[\\]]+");
    private static final Pattern P_PHRASE = Pattern.compile("\"[^\"]+\"");
    private static final Pattern P_AND = Pattern.compile("(?i)and\\b");
    private static final Pattern P_OR = Pattern.compile("(?i)or\\b");
    private static final Pattern P_NOT = Pattern.compile("(?i)not\\b");
    private static final Pattern P_TO = Pattern.compile("(?i)to\\b");

    private final String input;
    private int pos;
    private String lastMatched;

    public Lexer(String input) {
        this.input = input != null ? input : "";
        this.pos = 0;
        this.lastMatched = null;
    }

    public List<Token> tokenize() {
        List<Token> tokens = new ArrayList<>();
        while (pos < input.length()) {
            skipWhitespace();
            if (pos >= input.length()) break;

            char c = input.charAt(pos);

            if (c == '(') { tokens.add(new Token(LPAR, "(")); pos++; continue; }
            if (c == ')') { tokens.add(new Token(RPAR, ")")); pos++; continue; }
            if (c == ':') { tokens.add(new Token(COLON, ":")); pos++; continue; }
            if (c == '[') { tokens.add(new Token(LBRACK, "[")); pos++; continue; }
            if (c == ']') { tokens.add(new Token(RBRACK, "]")); pos++; continue; }

            if (match(P_AND)) { tokens.add(new Token(AND, "AND")); continue; }
            if (match(P_OR))  { tokens.add(new Token(OR, "OR")); continue; }
            if (match(P_NOT)) { tokens.add(new Token(NOT, "NOT")); continue; }
            if (match(P_TO))  { tokens.add(new Token(TO, "TO")); continue; }

            if (match(P_FIELD)) {
                tokens.add(new Token(FIELD, lastMatched));
                continue;
            }
            if (match(P_PHRASE)) {
                String v = lastMatched;
                tokens.add(new Token(PHRASE, v != null && v.length() > 2 ? v.substring(1, v.length() - 1) : ""));
                continue;
            }
            if (match(P_WORD)) {
                tokens.add(new Token(WORD, lastMatched != null ? lastMatched : ""));
                continue;
            }

            throw new IllegalArgumentException("Unexpected character at position " + pos + ": '" + c + "'");
        }
        tokens.add(new Token(EOF, ""));
        return tokens;
    }

    private void skipWhitespace() {
        while (pos < input.length() && Character.isWhitespace(input.charAt(pos))) pos++;
    }

    private boolean match(Pattern p) {
        Matcher m = p.matcher(input);
        if (!m.find(pos) || m.start() != pos) return false;
        lastMatched = input.substring(m.start(), m.end());
        pos = m.end();
        return true;
    }
}
