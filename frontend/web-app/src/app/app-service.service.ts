import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable()
export class AppServiceService {

  private readonly URL1 = "http://localhost:3000/"
  private readonly URL2 = "http://localhost:3000/snapshot"

  constructor(
    protected httpClient: HttpClient,
  ) {}

  public getMyOrderBook() {
    return this.httpClient.get(`${this.URL1}`);
  }

  public getCustomOrderBook(price, exchange) {
    var url = this.URL2 + "?price=" + price + "&exchange=" + exchange
    return this.httpClient.get(url);
  }

}