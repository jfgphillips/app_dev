# This is a sample Python script.
# Arbitrage strategy finding undervalued premium brands through market knowledge and automation

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from ParserClassEbay import ParserClass
from dataCategories import DataCategories
from applicationIO import applicationIO


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    search_list = ["ipad air 3rd generation", "bose quiet comfort 3"]
    parent_directory = "/Users/john/Documents/app development/parsed files"
    for search_term in search_list:
        test = ParserClass(search_term, 1)
        print(test.so_url)
        print(test.so_df)
        #graph = AnalysisClass(test.li_df, test.so_df)
        tst2 = applicationIO(search_term, parent_directory)
        filepath1, filepath2 = tst2.file_save(test.li_df, test.so_df)
        print(filepath1)
        print(filepath2)



    #list_df, sold_df = tst2.file_import('/Users/john/Documents/app development/parsed files/eBay fitbit charge 4 22-12-20 at 15.23/current private sellers of the fitbit charge 4.csv', '/Users/john/Documents/app development/parsed files/eBay fitbit charge 4 22-12-20 at 15.23/sold private sellers of the fitbit charge 4.csv')

    #tst3 = DataCategories(list_df, sold_df)
    #print(tst3.getAuction_df())
    #print(tst3.getSold_auction_df())
    #print(tst3.getSold_buy_now_df())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
