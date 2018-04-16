import { Routes } from '@angular/router';
import {SnapshotComponent} from "./snapshot/snapshot.component";
import {RealtimeComponent} from "./realtime/realtime.component";

export const routes: Routes = [
  { path: '', component: RealtimeComponent },
  { path: 'snapshot', component: SnapshotComponent }
];

