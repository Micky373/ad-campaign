# Importing useful libraries
import pandas as pd # For dataframe related tasks
import streamlit as st # For our webapp
import seaborn as sns # For data visualization
import matplotlib.pyplot as plt # For data visualizations

# Disabling warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

# Creating a header for our presentation
st.title("Data Visualization for Ad-Campaign")

# Creating a place where a user can drag and drop csv files
uploaded_file = st.file_uploader("Drag and drop a CSV file here")

def do_analysis():
    df = pd.read_csv(uploaded_file)
    # # Editing the data
    # df.loc[df['Start'] == 101,'Start'] = '1/01'
    # df.loc[df['Stop'] == 131,'Stop'] = '1/31'
    # Displaying the whole dataset
    st.dataframe(df)

    # Taking only some of the useful columns
    useful_columns = list(df.columns)
    columns_to_be_removed = [
        'CPL-TRAE',
    'CPL-ACT', 
        'Dur-C', 
        'Elap-C',
        'C-Actual', 
        'CPL-A', 
        'CLF'
    ]

    for column in columns_to_be_removed:
        useful_columns.remove(column)

    # Taking only portion of our dataset
    st.header("This is the useful data that we are going to analyze:")
    st.dataframe(df[useful_columns])

    # Let us change some columns to date time and the invoice into object
    df['Invoice'] = df['Invoice'].astype('object')
    # df['Start'] = pd.to_datetime(df['Start']+'/2023', format='%m/%d/%Y')
    # df['Stop'] = pd.to_datetime(df['Stop']+'/2023', format='%m/%d/%Y')

    # Let us see all unique values in our non-numerical columns
    st.header("Non-numerical Columns Analysis")
    for column in useful_columns:
        if df[column].dtype == 'O':
            st.write(f"Unique values in {column} column are -->\
            {df[column].unique()}")

    # Let us see statstical values of our numerical values
    st.header("Numerical Columns Analysis")
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    st.table(df[num_cols].describe())

    # Scatter plots of actual vs budget
    # This will help us to see if we are under or over budget spending

    fig, ax = plt.subplots()
    ax.scatter(df['Budget'], df['Actual'])
    ax.set_xlabel('Budget')
    ax.set_ylabel('Actual')
    ax.set_title('Actual vs Budget')

    # Displaying the plot
    st.header("Actual budget and the total budget comparision")
    st.pyplot(fig)

    # Grouping our leads by type of media and market

    leads_by_silo = df.groupby('Silo')['Ad-Leads'].sum()
    leads_by_market = df.groupby('Market')['Ad-Leads'].sum()

    # Plotting bar chart of the leads
    # This will help us see market and media effect on leads

    fig, ax = plt.subplots(2, 1, figsize=(10, 12))
    leads_by_silo.plot(kind='bar', ax=ax[0])
    ax[0].set_xlabel('Silo')
    ax[0].set_ylabel('Leads')
    ax[0].set_title('Leads Generated by Media')

    leads_by_market.plot(kind='bar', ax=ax[1])
    ax[1].set_xlabel('Market')
    ax[1].set_ylabel('Leads')
    ax[1].set_title('Leads Generated by Market')

    plt.tight_layout()
    st.header("Leads, Market and media relations")
    st.pyplot(fig)

    # Grouping the leads by status, market and media type

    leads_by_status_silo = df.groupby(['Status', 'Silo'])['Ad-Leads'].sum().unstack()
    leads_by_status_market = df.groupby(['Status', 'Market'])['Ad-Leads'].sum().unstack()

    # Plot to display leads generated by status, media type and market

    fig, ax = plt.subplots(2, 1, figsize=(10, 12))
    leads_by_status_silo.plot(kind='bar', stacked=True, ax=ax[0])
    ax[0].set_xlabel('Status')
    ax[0].set_ylabel('Leads')
    ax[0].set_title('Leads Generated by Status and Media')

    leads_by_status_market.plot(kind='bar', stacked=True, ax=ax[1])
    ax[1].set_xlabel('Status')
    ax[1].set_ylabel('Leads')
    ax[1].set_title('Leads Generated by Status and Market')

    plt.tight_layout()
    st.pyplot(fig)

    # Checking how our spent budget is creating a lead
    # This will help us identify how we are actually speding for leads

    fig , ax = plt.subplots()
    ax.scatter(df['Actual'],df['Leads'])
    ax.set_xlabel('Actual Spend')
    ax.set_ylabel('Leads Generated')
    ax.set_title('Actual Spend vs Leads Generated')

    st.header("Leads generated vs Budget currently spent relation")
    st.pyplot(fig)

    # Checking the distribution of cost per lead
    # This will help us identify how we are spending per lead averagely
    fig , ax = plt.subplots()
    ax.hist(df['CPL-G'])
    ax.set_xlabel('Cost per Lead')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Cost per Lead')

    st.header("Cost per leads distribution")
    st.pyplot(fig)

    # Group by media or Market and sum the budget components
    grouped = df.groupby('Silo')[['Budget', 'Actual']].sum()

    # Plot stacked bar chart
    ax = grouped.plot(kind='bar', stacked=True, figsize=(10,6))

    # Set plot title and axis labels
    ax.set_title('Budget Allocation by Media')
    ax.set_xlabel('Silo')
    ax.set_ylabel('Budget')

    st.header("Budget allocation for each media")
    st.pyplot(plt.gcf())

    # Displaying the success rate per client

    target_df = df.groupby('Client')['Target','Leads'].mean()

    fig, ax = plt.subplots()
    ax.bar(target_df.index, (target_df['Leads']/target_df['Target'])*100)
    ax.set_xlabel('Client')
    ax.set_ylabel('Success Rate in percent')
    ax.set_title('Success Rate per Client')

    # Display plot in Streamlit
    st.header("Success rate of our campaign in percent per each client")
    st.pyplot(fig)

# Load the data when a file is uploaded
if uploaded_file is not None:
    do_analysis()