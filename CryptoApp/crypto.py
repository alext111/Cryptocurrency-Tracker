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

    def addCoin(self, coin):
        db = self.connectDB()
        cursor = db.cursor()

        # queries to check if data columns for entered cryptocurrency exist, create if not already existing
        checkExistingPrice = 'ALTER TABLE crypto_table ADD COLUMN IF NOT EXISTS ' + coin + '_price MONEY;'
        checkExistingBalance = 'ALTER TABLE crypto_table ADD COLUMN IF NOT EXISTS ' + coin + '_balance MONEY;'
        checkExistingInitial = 'ALTER TABLE crypto_table ADD COLUMN IF NOT EXISTS ' + coin + '_initial MONEY;'
        checkExistingChange = 'ALTER TABLE crypto_table ADD COLUMN IF NOT EXISTS ' + coin + '_change DECIMAL(5,2);'
        checkExistingCoins = 'ALTER TABLE crypto_table ADD COLUMN IF NOT EXISTS ' + coin + '_coins DECIMAL(12,6);'

        # try checking of column for entered cryptocurrency exists, rollback if error occurs
        try:
            cursor.execute(checkExistingPrice)
            cursor.execute(checkExistingBalance)
            cursor.execute(checkExistingChange)
            cursor.execute(checkExistingInitial)
            cursor.execute(checkExistingCoins)
            db.commit()
            print('Columns successfully checked')
        except:
            print('Error in column checking')
            db.rollback()

        cursor.close()
        db.close()

    def fillEmptyRow(self, coin):
        db = self.connectDB()
        cursor = db.cursor()

        # queries to check if data columns for entered cryptocurrency exist, create if not already existing
        getRows = 'SELECT json_agg(crypto_table) FROM crypto_table;'

        # try checking of column for entered cryptocurrency exists, rollback if error occurs
        try:
            cursor.execute(getRows)
            data = cursor.fetchall()
            print(data)
            data = data[0][0][0]
            db.commit()
            print('Data successfully obtained')
        except:
            print('Error in data checking')
            db.rollback()

        print(data)
        for columnName in data:
            if data[columnName] == None:
                query = 'UPDATE crypto_table SET ' + columnName + ' = 0;'
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

        priceQuery = 'SELECT ' + coin + '_balance FROM crypto_table;'
        try:
            cursor.execute(priceQuery)
            balance = cursor.fetchall()
            db.commit()
            print('Balance successfully obtained from database')
            print(balance[0][0])
            print(type(balance[0][0]))
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

        coinQuery = 'SELECT ' + coin + '_coins FROM crypto_table;'
        try:
            cursor.execute(coinQuery)
            numCoins = cursor.fetchall()
            db.commit()
            print('Number of coins successfully obtained from database')
            print(numCoins[0][0])
            print(type(numCoins[0][0]))
            return numCoins[0][0]

        except:
            print('Error in coin check in database')
            db.rollback()

        cursor.close()
        db.close()

    def getInitial(self, coin):
        # obtain initial deposit from database
        db = self.connectDB()
        cursor = db.cursor()

        initialQuery = 'SELECT ' + coin + '_initial FROM crypto_table;'
        try:
            cursor.execute(initialQuery)
            initial = cursor.fetchall()
            db.commit()
            print('Initial deposit successfully obtained from database')
            print(initial[0][0])
            print(type(initial[0][0]))
            initial = self.currencyToNum(initial[0][0])
            return initial
        except:
            print('Error in initial deposit check in database')
            db.rollback()

        cursor.close()
        db.close()

    def getPriceAPI(self, coin):
        # obtain current price of selected cryptocurrency
        price = requests.get(
            'https://api.coingecko.com/api/v3/coins/' + coin + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
        price = price.json()
        print(price['market_data']['current_price']['usd'])
        return price['market_data']['current_price']['usd']

    def updateBalance(self, coin):
        # updates database price value with current value
        balance = self.calculateBalance(coin)
        print(balance)

        db = self.connectDB()
        cursor = db.cursor()

        balanceQuery = 'UPDATE crypto_table SET ' + coin + '_balance = ' + str(balance) + ';'
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
        print(change)

        db = self.connectDB()
        cursor = db.cursor()

        changeQuery = 'UPDATE crypto_table SET ' + coin + '_change = ' + str(change) + ';'
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
        # updates database initial deposit value with current value
        coins = self.calculateCoins(coin, difference)
        print(coins)

        db = self.connectDB()
        cursor = db.cursor()

        coinsQuery = 'UPDATE crypto_table SET ' + coin + '_coins = ' + str(coins) + ';'
        try:
            cursor.execute(coinsQuery)
            db.commit()
            print('Coins successfully updated')
        except:
            print('Error in coins update')
            db.rollback()

        cursor.close()
        db.close()

    def updateInitial(self, coin, difference):
        # updates database initial deposit value with current value
        initial = self.calculateInitial(coin, difference)
        print(initial)

        db = self.connectDB()
        cursor = db.cursor()

        initialQuery = 'UPDATE crypto_table SET ' + coin + '_initial = ' + str(initial) + ';'
        try:
            cursor.execute(initialQuery)
            db.commit()
            print('Initial deposit successfully updated')
        except:
            print('Error in initial deposit update')
            db.rollback()

        cursor.close()
        db.close()

    def updatePrice(self, coin):
        # updates database price value with current value
        price = self.getPriceAPI(coin)
        print(price)

        db = self.connectDB()
        cursor = db.cursor()

        priceQuery = 'UPDATE crypto_table SET ' + coin + '_price = ' + str(price) + ';'
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
        print(balance)
        return balance

    def calculateCoins(self, coin, difference):
        # obtain coins from db and use price to calculate new coins from deposit/withdrawal
        coins = self.getCoins(coin)
        price = self.getPriceAPI(coin)
        coins = difference/price + float(coins)
        if coins < 0:
            coins = 0
        print(coins)
        return coins

    def calculateInitial(self, coin, difference):
        # obtain initial deposit from db and calculate new initial based on deposit/withdrawal
        initial = self.getInitial(coin)
        initial = initial + difference
        if initial < 0:
            initial = 0
        print(initial)
        return initial

    def calculatePercentage(self, coin):
        #obtain initial deposit from db and balance to calculate percent change
        initial = self.getInitial(coin)
        balance = self.calculateBalance(coin)
        if initial == 0:
            percentage = 0
        else:
            percentage = (balance - initial)/initial * 100
        print(percentage)
        return percentage

    def currencyToNum(self, currency):
        #converts currency string to decimal float
        currency = re.sub(',', '', currency)
        currency = decimal.Decimal(currency.strip('$'))
        print(currency)
        return currency

#testing section
'''
app = CryptoApp()
app.addCoin("bitcoin")
app.fillEmptyRow("bitcoin")
app.updatePrice("bitcoin")
#app.updateInitial("bitcoin", 10000000)
#app.updateCoins("bitcoin", 10000000)
app.updateBalance("bitcoin")
app.updateChange("bitcoin")
app.addCoin("ethereum")
app.fillEmptyRow("ethereum")
app.updatePrice("ethereum")
'''