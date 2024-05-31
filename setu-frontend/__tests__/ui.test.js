import Home from '@/app/page'
import AAChartContainer from '@/components/Chart/AAChartContainer'
import SingleAAChart from '@/components/Chart/SingleAAChart';
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import config from "@/config/config.json";


// Mock RezizeObserver, 
// because the js-dom throws error `ResizeObserver` is not defined
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Sample docs
const SAMPLE_DOC = {
  "date": "01-01-17",
  "aas_data": {
    "Anumati": { "na_count": 59, "live_count": 53, "testing_count": 0 },
    "CAMS": { "na_count": 59, "live_count": 53, "testing_count": 0 },
    "CRIF": { "na_count": 81, "live_count": 29, "testing_count": 2 },
    "Digio": { "na_count": 106, "live_count": 3, "testing_count": 3 },
    "Finvu": { "na_count": 58, "live_count": 52, "testing_count": 2 },
    "INK": { "na_count": 80, "live_count": 28, "testing_count": 4 },
    "NADL": { "na_count": 61, "live_count": 46, "testing_count": 5 },
    "Onemoney": { "na_count": 37, "live_count": 73, "testing_count": 2 },
    "PhonePe": { "na_count": 91, "live_count": 10, "testing_count": 11 },
    "Protean SurakshAA": { "na_count": 74, "live_count": 35, "testing_count": 3 },
    "Setu AA": { "na_count": 100, "live_count": 10, "testing_count": 2 },
    "Saafe": { "na_count": 71, "live_count": 39, "testing_count": 2 },
    "TallyEdge": { "na_count": 91, "live_count": 18, "testing_count": 3 },
    "Yodlee": { "na_count": 102, "live_count": 7, "testing_count": 3 },
  },
}


// UI test case
describe('UI', () => {

  // Whether the website heading is rendered?
  it('Render website heading', () => {
    render(<Home />)
    expect(screen.getByText('Setu - AA trends')).toBeInTheDocument();
  })

  // Whether the 'loading...' text is rendered initially?
  it('Chart container render without data', () => {
    render(<AAChartContainer />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  // The no. of charts == the number of AAs present in sample data?
  it('Chart container render with mock data', () => {

    const data = new Array(4).fill(SAMPLE_DOC)
    render(<AAChartContainer mockData={data} />)
    const chartContainer = screen.getByTestId('chart-container-id');
    expect(chartContainer.children.length).toBe(Object.keys(SAMPLE_DOC.aas_data).length)
  })

  // The no. of charts with empty data == the number of AAs present in mock config?
  it('Chart container render with empty data', () => {

    render(<AAChartContainer mockData={[]} />)
    const chartContainer = screen.getByTestId('chart-container-id');
    expect(chartContainer.children.length).toBe(config.mock.aaNames.length)
  })


  // Whether single aa chart is throwing any errors?
  it('Render single chart with mock data', () => {

    const data = new Array(4).fill(SAMPLE_DOC);
    render(<SingleAAChart aaName={"Setu AA"} aaData={data} addMockData={true}  />)
  })

})