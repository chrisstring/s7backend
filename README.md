s7backend handles all the scripts for creating the framework of the interface used to interact with s7

>interface.py

This interface handles most of the functions

**To Do:**

- [ ] Build authUser
>  authUser accepts user credentials and verifies them with scene7's verification system

- [ ] Build readCSV function
> readCSV will use the built in csv reader module to read a CSV of skus that need to be searched.  Each sku is then passed to the singleSkuSearch function

- [ ] Build singleSkuSearch function
> singleSkuSearch receives a single SKU from the readCSV function and passes it in the SOAP object which then receives an XML array of data back.

- [ ] Build readResultsArray
> readResultsArray accepts the XML data array back and parses through it to get all of the relevant asset names back (may return a tuple of tuples or an array).  readResultsArray will then iterate through each of the assets (J100109 -> J100109_alt1, etc) calling on addToQueue to check the current queue size

- [ ] Build addToQueue search function
- [ ] Build createJob function
- [ ] Build submitJob function
