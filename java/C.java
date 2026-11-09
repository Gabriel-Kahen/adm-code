import java.io.IOException;
import java.util.Locale;

/** Java equivalents of the C examples' stdio and string primitives. */
final class C {
    static int errno;
    private static final java.io.BufferedInputStream input = new java.io.BufferedInputStream(System.in);
    private static int lookahead = -2;
    private static final String[] values = new String[32];
    private static int peek() {
        if (lookahead == -2) {
            try { lookahead = input.read(); }
            catch (IOException e) { throw new java.io.UncheckedIOException(e); }
        }
        return lookahead;
    }
    static int getchar() { int value = peek(); lookahead = -2; return value; }
    private static boolean space(int value) { return value >= 0 && " \t\n\r\f\013".indexOf(value) >= 0; }
    private static boolean digit(int value) { return value >= '0' && value <= '9'; }
    static int scan(String format) {
        int count = 0;
        for (int i = 0; i < format.length(); i++) {
            char f = format.charAt(i);
            if (Character.isWhitespace(f)) {
                while (space(peek())) getchar();
            } else if (f == '%') {
                int width = 0;
                while (i + 1 < format.length() && Character.isDigit(format.charAt(i + 1))) width = width * 10 + format.charAt(++i) - '0';
                while (i + 1 < format.length() && (format.charAt(i + 1) == 'l' || format.charAt(i + 1) == 'h')) i++;
                char type = format.charAt(++i);
                if (type != 'c') while (space(peek())) getchar();
                if (peek() < 0) return count == 0 ? -1 : count;
                StringBuilder value = new StringBuilder();
                if (type == 'c') value.append(getchar());
                else if (type == 's') {
                    while (peek() >= 0 && !space(peek()) && (width == 0 || value.length() < width)) value.append((char)getchar());
                } else {
                    if (peek() == '+' || peek() == '-') value.append((char)getchar());
                    boolean digits = false;
                    while (digit(peek())) { value.append((char)getchar()); digits = true; }
                    if (type != 'd' && type != 'u') {
                        if (peek() == '.') {
                            value.append((char)getchar());
                            while (digit(peek())) { value.append((char)getchar()); digits = true; }
                        }
                        if (digits && (peek() == 'e' || peek() == 'E')) {
                            value.append((char)getchar());
                            if (peek() == '+' || peek() == '-') value.append((char)getchar());
                            while (digit(peek())) value.append((char)getchar());
                        }
                    }
                    if (!digits) return count;
                }
                values[count++] = value.toString();
            } else {
                if (peek() != f) return count;
                getchar();
            }
        }
        return count;
    }
    static int scanInt(int i) { return Integer.parseInt(values[i]); }
    static long scanLong(int i) { return Long.parseLong(values[i]); }
    static double scanDouble(int i) { return Double.parseDouble(values[i]); }
    static char[] scanString(int i) { return (values[i] + '\0').toCharArray(); }
    static int strlen(char[] s) { int n = 0; while (n < s.length && s[n] != 0) n++; return n; }
    static int strlen(char[] s, int offset) { int n = offset; while (n < s.length && s[n] != 0) n++; return n - offset; }
    static int strcmp(char[] a, char[] b) {
        int i = 0;
        while (i < a.length && i < b.length && a[i] != 0 && a[i] == b[i]) i++;
        return (i == a.length ? 0 : a[i]) - (i == b.length ? 0 : b[i]);
    }
    static void strcpy(char[] dest, char[] source) { int i = 0; do { dest[i] = i < source.length ? source[i] : 0; } while (dest[i++] != 0); }
    static void perror(String label) { System.err.println(label + ": " + (errno == 33 ? "Numerical argument out of domain" : errno == 34 ? "Numerical result out of range" : "Success")); }
    // Mutable NUL-terminated buffers and C booleans need explicit formatting.
    static void printf(String format, Object... args) {
        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof char[]) {
                char[] value = (char[])args[i];
                args[i] = new String(value, 0, strlen(value));
            } else if (args[i] instanceof Boolean) {
                args[i] = (Boolean)args[i] ? 1 : 0;
            }
        }
        System.out.printf(Locale.US, format, args);
    }
    private C() {}
}
