export class SearchResponseModel {
    fixedWord: string;
    productsDetails: ProductDetailsModel[] = [];
}

export class ProductDetailsModel {
    // tslint:disable-next-line: variable-name
    Product_Generic_Name: string;
    // tslint:disable-next-line: variable-name
    Product_ID: string;
    // tslint:disable-next-line: variable-name
    Product_Img_Url: string;
    // tslint:disable-next-line: variable-name
    Product_Link: string;
    // tslint:disable-next-line: variable-name
    Product_Name: string;
    // tslint:disable-next-line: variable-name
    Product_Price: number;
    // tslint:disable-next-line: variable-name
    Product_Rating: string;
    // tslint:disable-next-line: variable-name
    Product_Highlights: ProductHighlightsModel[] = [];
}

class ProductHighlightsModel {
    highlight: string;
}
