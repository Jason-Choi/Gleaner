import { batch, effect, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { InitResponse } from '../types/API';
import { ChartType } from '../types/ChartType';
import { attributesSignal } from './attribute';
import { chartTypesSignal } from './chartType';
import { selectedTaskTypeSignal, taskTypesSignal } from './taskType';
import { transformationsSignal } from './transformation';
import { trainGleaner } from './train';
import { inferDashboard } from './infer';

const initializedSignal = signal<boolean>(false);

const init = async (datasetName: string = 'Movies') => {
  const response: InitResponse = (
    await axios.get(`${URI}/init?name=${datasetName}`)
  ).data;
  batch(() => {
    trainGleaner();
    inferDashboard();
    attributesSignal.value = response.attributes.map((attribute) => {
      return {
        ...attribute,
        prefer: false,
        ignore: false,
      };
    });
    chartTypesSignal.value = response.chartTypes.map((chartType) => {
      return {
        ...chartType,
        prefer: false,
        ignore: false,
      };
    });
    transformationsSignal.value = response.transformations.map(
      (transformation) => {
        return {
          ...transformation,
          prefer: false,
          ignore: false,
        };
      },
    );
    // taskTypesSignal.value = response.taskTypes.map((taskType) => {
    //     return {
    //         ...taskType,
    //         chartTypes: taskType.chartTypes.map((chartType) => chartTypesSignal.peek().find((ct) => ct.name === chartType.name) as ChartType),
    //     };
    // });
    // selectedTaskTypeSignal.value = { ...selectedTaskTypeSignal.peek(), chartTypes: chartTypesSignal.peek() }
    initializedSignal.value = true;
  });
  initializedSignal.value = true;
};

effect(() => {
  init();
})();

export { initializedSignal, init };
