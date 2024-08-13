# SaaS Platform for Sourcing Agents

## Description

This SaaS platform enables freelance sourcing agents to manage their supplier contacts, create and manage RFI/RFQ documents, and track key performance indicators (KPIs) through a dashboard. The MVP uses Streamlit for the user interface and Firebase for data management (MongoDB on the mongo branch).

## Features

1. **Supplier Contact Management**
   - Add, edit, delete, and view suppliers.
2. **RFI/RFQ Document Management**
   - Create, edit, delete, and view RFI (Request for Information) and RFQ (Request for Quotation) documents.
3. **Dashboard - KPI**
   - Display key KPIs such as the total number of suppliers, RFIs, and RFQs.

## Technologies Used

- [Streamlit](https://streamlit.io/): For building the user interface.
- [Firebase](https://firebase.google.com/): For database management (MongoDB on the mongo branch).
- [Python](https://www.python.org/): The main programming language.

## Prerequisites

- Python 3.x installed on your machine.
- A Firebase account and a project configured with the Admin SDK.
- The required Python libraries (see below).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure Firebase:

    - Add your `firebase_config.json` configuration file to the project directory.

4. Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

## Usage

### Home

On the homepage, you will find a brief introduction and description of the platform.

### Contact Management

- Navigate to the "Contact Management" section in the navigation menu.
- Use the form to add new suppliers.
- View the list of registered suppliers.

### RFI/RFQ Documents

- Navigate to the "RFI/RFQ Documents" section in the navigation menu.
- Select the document type (RFI or RFQ).
- Use the form to add new documents.
- View the list of registered documents.

### Dashboard - KPI

- Navigate to the "Dashboard" section in the navigation menu.
- Review key KPIs to monitor the performance of sourcing activities.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Authors

- Jérôme COFFIN -

## Acknowledgments

- Thanks to the Streamlit and Firebase communities for their excellent documentation and support.
