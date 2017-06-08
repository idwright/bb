import { BackboneClientPage } from './app.po';

describe('backbone-client App', () => {
  let page: BackboneClientPage;

  beforeEach(() => {
    page = new BackboneClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
