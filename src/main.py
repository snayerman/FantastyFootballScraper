import scrapeNarffl
import scrapePickem

def main():
   narffl = scrapeNarffl.main()
   pickem = scrapePickem.main()

   print "Narffl: {0}\n".format(narffl)
   print "Pickem: {0}\n".format(pickem)

if __name__ == "__main__":
    main()