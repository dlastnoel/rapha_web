const appointmentLabels = [
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
  'Sunday'
];
const apointmentData = {
  labels: appointmentLabels,
  datasets: [{
    label: 'APPOINMENTSS DONE BY DAY',
    backgroundColor: 'rgb(7, 174, 217)',
    borderColor: 'rgb(7, 174, 217)',
    data: [0, 10, 5, 2, 20, 30, 45, 66],
  }]
};
const appoinmentConfigs = {
  type: 'bar',
  data: apointmentData,
  options: {}
};

const appointmentChart = new Chart(
document.getElementById('appointmentChart'),
appoinmentConfigs
);