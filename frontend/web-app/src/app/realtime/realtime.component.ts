import { Component, OnInit } from '@angular/core';
import {AppServiceService} from "../app-service.service";

@Component({
  selector: 'app-realtime',
  templateUrl: './realtime.component.html',
  styleUrls: ['./realtime.component.css']
})
export class RealtimeComponent implements OnInit {
  data: any = [];

  constructor(private appService: AppServiceService) {}

  ngOnInit() {
    setInterval(() => {

      this.appService.getMyOrderBook().subscribe(data => this.data = data);
    }, 400);
  }

}