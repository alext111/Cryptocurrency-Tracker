import requests
import psycopg2
import decimal
import re

class CryptoApp():

    def connectDB(self):
        # create connection to postgresql database
        db = psycopg2.connect(
            host='localhost',
            database='cryptodb',
            user='testuser',
            password='testpw')
        return db

    def addCoinRow(self, coin):
        db = self.connectDB()
        cursor = db.cursor()

        #query to check if row with coin name already exists, else add row
        checkExistingName = """INSERT INTO "cryptoFront_coininfo"(name) SELECT '""" + coin + """' WHERE NOT EXISTS (SELECT 1 FROM "cryptoFront_coininfo" WHERE name = '""" + coin + "');"

        # try checking of column for entered cryptocurrency exists, rollback if error occurs
        try:
            cursor.execute(checkExistingName)
            db.commit()
            print('Rows successfully checked')
        except:
            print('Error in row checking')
            db.rollback()

        cursor.close()
        db.close()

    def fillEmptyRow(self, coin):
        db = self.connectDB()
        cursor = db.cursor()

        # queries to check if data columns for entered cryptocurrency exist, create if not already existing
        getRows = """SELECT json_agg("cryptoFront_coininfo") FROM "cryptoFront_coininfo" where name = '""" + coin + "';"

        # try checking of column for entered cryptocurrency exists, rollback if error occurs
        try:
            cursor.execute(getRows)
            data = cursor.fetchall()
            data = data[0][0][0]
            db.commit()
            print('Data successfully obtained')
        except:
            print('Error in data checking')
            db.rollback()

        for columnName in data:
            if data[columnName] == None:
                query = 'UPDATE "cryptoFront_coininfo" SET ' + columnName + " = 0 WHERE name = '" + coin + "';"
                try:
                    cursor.execute(query)
                    db.commit()
                    print(columnName + ' value updated')
                except:
                    print('Error in null value update')
                    db.rollback()

        cursor.close()
        db.close()

    def getBalanceDB(self, coin):
        # obtain balance value from database
        db = self.connectDB()
        cursor = db.cursor()

        balanceQuery = """SELECT balance FROM "cryptoFront_coininfo" WHERE name = '""" + coin + "';"
        try:
            cursor.execute(balanceQuery)
            balance = cursor.fetchall()
            db.commit()
            print('Balance successfully obtained from database')
            return balance[0][0]

        except:
            print('Error in balance check in database')
            db.rollback()

        cursor.close()
        db.close()

    def getCoins(self, coin):
        # obtain number of coins from database
        db = self.connectDB()
        cursor = db.cursor()

        coinQuery = """SELECT coins FROM "cryptoFront_coininfo" WHERE name = '""" + coin + "';"
        try:
            cursor.execute(coinQuery)
            numCoins = cursor.fetchall()
            db.commit()
            print('Number of coins successfully obtained from database')
            numCoins = float(numCoins[0][0])
            return numCoins

        except:
            print('Error in coin check in database')
            db.rollback()

        cursor.close()
        db.close()

    def getDeposit(self, coin):
        # obtain deposit from database
        db = self.connectDB()
        cursor = db.cursor()

        depositQuery = """SELECT deposit FROM "cryptoFront_coininfo" WHERE name = '""" + coin + "';"
        try:
            cursor.execute(depositQuery)
            deposit = cursor.fetchall()
            db.commit()
            print('Deposit successfully obtained from database')
            deposit = self.currencyToNum(deposit[0][0])
            return deposit
        except:
            print('Error in deposit check in database')
            db.rollback()

        cursor.close()
        db.close()

    def getPriceAPI(self, coin):
        # obtain current price of selected cryptocurrency
        price = requests.get(
            'https://api.coingecko.com/api/v3/coins/' + coin + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
        price = price.json()

        return price['market_data']['current_price']['usd']

    def updateBalance(self, coin):
        # updates database price value with current value
        balance = self.calculateBalance(coin)

        db = self.connectDB()
        cursor = db.cursor()

        balanceQuery = 'UPDATE "cryptoFront_coininfo" SET balance = ' + str(balance) + " WHERE name = '" + coin + "';"
        try:
            cursor.execute(balanceQuery)
            db.commit()
            print('Balance successfully updated')
        except:
            print('Error in balance update')
            db.rollback()

        cursor.close()
        db.close()

    def updateChange(self, coin):
        # updates database percentage change value with current value
        change = self.calculatePercentage(coin)

        db = self.connectDB()
        cursor = db.cursor()

        changeQuery = 'UPDATE "cryptoFront_coininfo" SET change = ' + str(change) + " WHERE name = '" + coin + "';"
        try:
            cursor.execute(changeQuery)
            db.commit()
            print('Percentage change successfully updated')
        except:
            print('Error in percentage change update')
            db.rollback()

        cursor.close()
        db.close()

    def updateCoins(self, coin, difference):
        # updates database coin value with current value
        coins = self.calculateCoins(coin, difference)

        db = self.connectDB()
        cursor = db.cursor()

        coinsQuery = 'UPDATE "cryptoFront_coininfo" SET coins = ' + str(coins) + " WHERE name = '" + coin + "';"
        try:
            cursor.execute(coinsQuery)
            db.commit()
            print('Coins successfully updated')
        except:
            print('Error in coins update')
            db.rollback()

        cursor.close()
        db.close()

    def updateDeposit(self, coin, difference):
        # updates database deposit value with current value
        deposit = self.calculateDeposit(coin, difference)

        db = self.connectDB()
        cursor = db.cursor()

        depositQuery = 'UPDATE "cryptoFront_coininfo" SET deposit = ' + str(deposit) + " WHERE name = '" + coin + "';"
        try:
            cursor.execute(depositQuery)
            db.commit()
            print('Deposit successfully updated')
        except:
            print('Error in deposit update')
            db.rollback()

        cursor.close()
        db.close()

    def updatePrice(self, coin):
        # updates database price value with current value
        price = self.getPriceAPI(coin)

        db = self.connectDB()
        cursor = db.cursor()

        priceQuery = 'UPDATE "cryptoFront_coininfo" SET price = ' + str(price) + " WHERE name = '" + coin + "';"
        try:

            cursor.execute(priceQuery)
            db.commit()
            print('Price successfully updated')
        except:
            print('Error in price update')
            db.rollback()

        cursor.close()
        db.close()

    def calculateBalance(self, coin):
        #obtain number of coins from db and price from api to calculate balance
        numCoins = self.getCoins(coin)
        price = self.getPriceAPI(coin)
        balance = numCoins*price
        return balance

    def calculateCoins(self, coin, difference):
        # obtain coins from db and use price to calculate new coins from deposit/withdrawal
        coins = self.getCoins(coin)
        price = self.getPriceAPI(coin)
        coins = difference/price + float(coins)
        if coins < 0:
            coins = 0
        return coins

    def calculateDeposit(self, coin, difference):
        # obtain deposit from db and calculate new deposit based on deposit/withdrawal
        deposit = self.getDeposit(coin)
        deposit = deposit + difference
        if deposit < 0:
            deposit = 0
        return deposit

    def calculatePercentage(self, coin):
        #obtain deposit from db and balance to calculate percent change
        deposit = self.getDeposit(coin)
        balance = self.calculateBalance(coin)
        if deposit == 0:
            percentage = 0
        else:
            percentage = (balance - deposit)/deposit * 100
        return percentage

    def currencyToNum(self, currency):
        #converts currency string to decimal float
        currency = re.sub(',', '', currency)
        currency = decimal.Decimal(currency.strip('$'))
        currency = float(currency)
        return currency
