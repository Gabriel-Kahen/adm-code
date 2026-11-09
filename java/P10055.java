/* Direct translation of 10055.c */

import java.util.Locale;

public class P10055 {

    public static int main() {
        long p = 0;
        long q = 0;
        long r = 0;
        while (true) {
            int _read0 = C.scan("%ld %ld");
            if (_read0 > 0) p = C.scanLong(0);
            if (_read0 > 1) q = C.scanLong(1);
            if (_read0 == -1) break;
            if ((q > p)) {
                r = (q - p);
            } else {
                r = (p - q);
            }
            System.out.printf(Locale.US, "%d\n", r);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
