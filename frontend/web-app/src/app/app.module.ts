import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from "@angular/common/http";
import { AppComponent } from './app.component';
import {AppServiceService} from "./app-service.service";
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { routes} from "./app.routes";
import { SnapshotComponent } from './snapshot/snapshot.component';
import { RealtimeComponent } from './realtime/realtime.component';

@NgModule({
  declarations: [
    AppComponent,
    SnapshotComponent,
    RealtimeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [AppServiceService],
  bootstrap: [AppComponent]
})
export class AppModule { }